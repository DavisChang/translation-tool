const fs = require("fs");
const path = require("path");
const csv = require("csv-parser");

const fileName = "en_web";
const csvFilePath = path.join(__dirname, "translations", `${fileName}.csv`);
const jsonFilePath = path.join(__dirname, `locales/web/${fileName}.json`);

// Ensure output directory exists
if (!fs.existsSync(path.dirname(jsonFilePath))) {
    fs.mkdirSync(path.dirname(jsonFilePath), { recursive: true });
}

// Read CSV and convert to JSON
const jsonData = {};
const orderedKeys = [];

fs.createReadStream(csvFilePath)
  .pipe(csv()) // Parses CSV file
  .on("data", (row) => {
    const key = row["Key"].trim();
    const englishValue = row["English Value"].trim();
    const chineseValue = row["Chinese Value"].trim(); // Get Chinese translation

    if (!jsonData[key]) {
      jsonData[key] = chineseValue || englishValue; // Use Chinese if available, otherwise fallback to English
      orderedKeys.push(key); // Preserve order
    }
  })
  .on("end", () => {
    // Sort JSON object based on the order of keys in the CSV
    const sortedJson = orderedKeys.reduce((acc, key) => {
      acc[key] = jsonData[key];
      return acc;
    }, {});

    // Save JSON file
    fs.writeFileSync(jsonFilePath, JSON.stringify(sortedJson, null, 2), "utf8");

    console.log("✅ JSON file has been created:", jsonFilePath);
  })
  .on("error", (error) => {
    console.error("❌ Error processing CSV:", error);
  });
