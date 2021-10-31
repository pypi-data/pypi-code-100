

class FeatureDescriptor:
    def __init__(
        self,
        feature_class_group: str,
        feature_class: str,
        feature_name: str,
        feature_id: str,
        pos_tags: str,
        documentation_link: str,
        statistics_link: str,
        standard,
    ):
        self.feature_class_group = feature_class_group
        self.feature_class = feature_class
        self.feature_name = feature_name
        self.feature_id = feature_id
        self.pos_tags = [pt.strip() for pt in pos_tags.split(",")]
        self.documentation_link = documentation_link
        self.statistics_link = statistics_link
        self.standard = standard

    def __eq__(self, other):
        if isinstance(other, FeatureDescriptor):
            return (
                self.feature_class_group == other.feature_class_group
                and self.feature_class == other.feature_class
                and self.feature_name == other.feature_name
                and self.feature_id == other.feature_id
                and self.documentation_link == other.documentation_link
                and self.statistics_link == other.statistics_link
            )
        return False

    def __str__(self):
        return f"{self.feature_class}:{self.feature_name} ({self.feature_id})"
