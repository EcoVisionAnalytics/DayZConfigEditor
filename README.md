# DayZ Trader Config Editor

A Streamlit web application for easily modifying DayZ mod configuration files, particularly focused on TraderPlus price configurations.

![DayZ Trader Config Editor](https://img.shields.io/badge/DayZ-Trader%20Config%20Editor-brightgreen)

## Features

- Upload and parse DayZ mod JSON configuration files
- View all trader categories and items in an organized interface
- Make bulk modifications:
  - Change all prices by a percentage (increase or decrease)
  - Set all stock levels at once
- View data in an organized tabular format
- Download the modified configuration file

## Installation

1. Make sure you have Python installed (3.8+ recommended)
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

### Local Usage

1. Run the Streamlit app:

```
streamlit run app.py
```

2. Open your web browser to the URL displayed in the terminal (typically http://localhost:8501)
3. Upload your TraderPlus configuration file
4. Make your desired changes using the sidebar controls
5. Apply changes as needed
6. Generate and download the modified file

### Online Usage (via Streamlit Cloud)

1. Visit the deployed app at: [Your Streamlit Cloud URL will go here]
2. Upload your TraderPlus configuration file
3. Make your changes and download the modified file

## Deployment

### Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Sign up for a free account at [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub account to Streamlit Cloud
4. Select this repository and deploy
5. Your app will be publicly accessible via a unique URL

## Future Enhancements

- Individual item editing
- Category-specific price adjustments
- Preset management for common configurations
- Support for other DayZ mod configuration formats
- Backup and restore functionality

## Notes

This tool is designed for the TraderPlus mod configuration format. It assumes the product entries follow the format:
`ItemName,Value2,Value3,StockValue,BuyPrice,SellPrice`

If your configuration uses a different format, you may need to modify the parsing logic in the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
