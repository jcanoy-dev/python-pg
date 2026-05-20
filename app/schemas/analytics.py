from typing import Optional
from pydantic import BaseModel, Field

class AnalyticsPayload(BaseModel):
    page_path: str = Field(..., description="The current URL path, e.g., '/projects/my-app'")
    referrer: Optional[str] = Field(default="direct", description="Where the user came from, e.g., 'linkedin.com'")
    event_category: Optional[str] = Field(default=None, description="Broad action class, e.g., 'outbound_link'")
    event_action: Optional[str] = Field(default=None, description="Specific action string, e.g., 'click_github'")
    event_label: Optional[str] = Field(default=None, description="Extra context meta, e.g., 'Portfolio Source Code Link'")

    model_config = {
        "json_schema_extra": {
            "example": {
                "page_path": "/projects/chat-app",
                "referrer": "github.com",
                "event_category": "button_click",
                "event_action": "download_resume",
                "event_label": "English CV PDF"
            }
        }
    }
