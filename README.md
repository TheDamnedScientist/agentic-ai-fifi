# FiFi

FiFi is a project located in this directory. Below is an overview of the folder structure and the purpose of each file/folder.

## Folder Structure

```
.
├── backend/            # Source code for backend
├── frontend/           # Source code for frontend
├── utils/              # Contains tools like fi-mcp-dev server, etc.
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
    Please setup the prerequisites from the official [git repo](https://github.com/epiFi/fi-mcp-dev/blob/master/README.md) and then in a separate shell/terminal, start the fi-mcp-dev server.

    ```bash
    cd utils/fi-mcp-dev
    go run .
    ```

    Post server start, run these commands from the root of the repo.

    To test mock flow, run:
    ```bash
    python -m backend.mock_flow.cli_mock
    ```

    To test the flow with Gemini integration, run:
    ```bash
    python -m backend.cli_gemini
    ```

## Running Tests

None as of now

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the terms described in the `LICENSE` file.