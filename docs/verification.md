# Verification and reproducibility

[Home](../README.md) · [Source manifest](../original-files/source-manifest.json) · [Verifier](../scripts/verify_package.py)

Run `python scripts/verify_package.py` from a local checkout using Python 3.9 or newer. It uses the standard library only.

The verifier checks relative Markdown links remain inside the repository and resolve, all 26 presentation sections appear in order, three source files match their recorded hashes and sizes, seven original plus six reviewed SPL files exist, and the reported byte arithmetic and time differences reconcile.

The portfolio contains no raw exercise dataset. Verification does not establish original log completeness, execute SPL, validate live IAM state, or independently corroborate the reported findings. The supplied sources were read as text with document tables and presentation notes included. Historical DOCX and HTML originals are preserved byte-for-byte rather than redesigned; no new PDF or PowerPoint rendering is claimed.

The complete local package is ready to copy into a repository. Public GitHub publication was authorized by the portfolio owner. No license grant was inferred for team/course source material.
