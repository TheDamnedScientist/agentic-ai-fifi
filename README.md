# FiFi

FiFi is a project located in this directory. Below is an overview of the folder structure and the purpose of each file/folder.

## Folder Structure

```
.
├── backend/            # Source code for backend
├── frontend/           # Source code for frontend
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── LICENSE             # License information
└── ...                 # Other files and folders
```

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/TheDamnedScientist/agentic-ai-fifi
    cd agentic-ai-fifi
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    Run these commands from the root of the repo.
    
    To test mock flow, run this
    ```bash
    python -m backend.mock_flow.cli_mock
    ```

    Run this for testing the flow with gemini integration
    ```bash
    python -m backend.cli_gemini
    ```

## Running Tests

None as of now

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the terms described in the `LICENSE` file.