
example_vars = """
title: How to make a cheeseburger
description: A simple step by step guide on how to make juicy burgers
disclaimer: I am not a professional. Any injury, disablement, or deaths caused by the burgers you consume are not my fault.
toc:
  - label: Get meat
    link: ./docs/meats.md
  - label: Cook meat
    link: ./docs/cooking.md
  - label: Enjoy
    link: ./docs/enjoy.md
"""

example_template = """
# {{ title }}

{{ description }}

> {{ disclaimer }}

{% if toc %}
{% for t in toc %}
- [{{ t.label }}]({{ t.link }})
{% endfor %}
{% endif %}

Author: [{{ name }}]({{ github_profile }})

Contact: [{{ email }}](mailto:{{ email }})
"""