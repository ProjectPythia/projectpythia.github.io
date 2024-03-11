# User Metrics

Total Users:

Portal: {{ jsonextract("../github/user_metrics.json", "$.portal") }}

Foundations: {{ jsonextract("../github/user_metrics.json", "$.foundations") }}

Cookbooks: {{ jsonextract("../github/user_metrics.json", "$.cookbooks") }}
