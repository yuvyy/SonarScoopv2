# 🔍 SonarScoop v2 - AI powered SonarQube Security Hotspots Analyzer and Exporter

LLM-Powered SonarQube Security Hotspot Reviewer is a tool that automates the analysis of security hotspots identified by SonarQube using a large language model (LLM). It extracts the relevant code segments flagged by SonarQube, sends them to an LLM for contextual understanding, and returns a verdict on whether each hotspot is a false positive or a valid security vulnerability.

## Each analysis includes:

- Verdict (False Positive or Valid Vulnerability)

- Detailed Observations

- Recommendation for mitigation or improvement

- Potential Impact


---

## 🚀 Usage

1. **Clone or Download** the script.

    ```bash
    git clone https://github.com/yuvyy/SonarScoopv2.git
    ```
2. **Open the folder**:

    ```bash
    cd SonarScoopv2
    ```
3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
4. **Run the script**:

    ```bash
    python main.py
    ```


