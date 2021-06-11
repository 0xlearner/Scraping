# 
import re
def sanitize_url(url: str) -> str:
    return re.sub(r"([^:]//)(/)+", r"\1", url)

url = "'\\https:\\\\lifebridgecapital.com\\2021\\06\\11\\ws964-multifamily-investing-is-a-team-sport-with-cameron-roy\\\\'"
print(sanitize_url(url))