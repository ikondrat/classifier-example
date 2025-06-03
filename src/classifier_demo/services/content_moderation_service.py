"""Content Moderation Service.

This service provides content moderation capabilities using a pre-trained transformer model.
It implements a singleton pattern to ensure efficient resource usage and includes rate limiting
functionality to track request rates.
"""

import logging
import time
from collections import deque
from threading import Lock
from typing import Deque, Dict, Optional

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class ContentModerationService:
    """Service for content moderation using a pre-trained transformer model.

    This class implements a singleton pattern to ensure only one instance of the model
    is loaded in memory. It provides methods for text moderation and request rate tracking.
    """

    _instance: Optional["ContentModerationService"] = None
    _initialized: bool = False

    # Mapping of model labels to human-readable categories
    CATEGORY_MAPPING: Dict[str, str] = {  # noqa: RUF012
        "H": "Hate Speech",
        "H2": "Hate Speech (Severe)",
        "HR": "Hate Speech (Racial)",
        "OK": "Safe Content",
        "S": "Sexual Content",
        "S3": "Sexual Content (Explicit)",
        "SH": "Sexual Harassment",
        "V": "Violence",
        "V2": "Violence (Severe)",
    }

    def __new__(cls, *args, **kwargs) -> "ContentModerationService":  # noqa: ARG004
        """Create or return the singleton instance of ContentModerationService.

        Returns:
            ContentModerationService: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "KoalaAI/Text-Moderation") -> None:
        """Initialize the content moderation service.

        Args:
            model_name: The name or path of the pre-trained model to use.
        """
        if not self._initialized:
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.eval()  # Set to evaluation mode

            # Initialize request tracking
            self.request_timestamps: Deque[float] = deque(maxlen=1000)  # Store last 1000 requests
            self.request_lock = Lock()
            self._initialized = True
            logger.info(
                "ContentModerationService initialized with model: %s",
                model_name,
            )

    @classmethod
    def initialize(cls, model_name: str = "KoalaAI/Text-Moderation") -> "ContentModerationService":
        """Initialize the service and download the model.

        Args:
            model_name: The name or path of the pre-trained model to use.

        Returns:
            ContentModerationService: The initialized service instance.
        """
        return cls(model_name)

    def get_request_rate(self) -> float:
        """Calculate the current request rate (requests per second) based on the last minute.

        Returns:
            float: The number of requests per second in the last minute.
        """
        current_time = time.time()
        one_minute_ago = current_time - 60

        with self.request_lock:
            # Remove requests older than one minute
            while self.request_timestamps and self.request_timestamps[0] < one_minute_ago:
                self.request_timestamps.popleft()

            # Calculate rate
            if not self.request_timestamps:
                return 0.0

            requests_per_second = len(self.request_timestamps) / 60.0
            logger.info("Current request rate: %.2f requests/second", requests_per_second)
            return requests_per_second

    def moderate_text(self, text: str) -> Dict[str, float]:
        """Process text through the moderation model and return category scores.

        Args:
            text: The text to be moderated.

        Returns:
            Dict[str, float]: A dictionary mapping category names to their confidence scores.
        """
        # Track request timestamp
        with self.request_lock:
            self.request_timestamps.append(time.time())

        # Tokenize and prepare input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)

        # Run inference
        with torch.no_grad():
            outputs = self.model(**inputs)
            confidence_scores = torch.sigmoid(outputs.logits).squeeze().numpy()

        # Get category labels and map them to human-readable categories
        category_labels = self.model.config.id2label

        # Create result dictionary with mapped categories
        return {
            self.CATEGORY_MAPPING.get(category_labels[i], category_labels[i]): float(score)
            for i, score in enumerate(confidence_scores)
        }

    def cleanup(self) -> None:
        """Clean up service resources and reset the singleton instance."""
        if self._initialized:
            logger.info("Cleaning up ContentModerationService resources.")
            self._initialized = False
            self._instance = None
        else:
            logger.warning("ContentModerationService is not initialized.")
