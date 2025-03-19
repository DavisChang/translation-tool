const fs = require("fs");
const path = require("path");

const fileName = 'en_web'
const filePath = path.join(__dirname, `../locales/web/${fileName}.json`);

try {
    // Read and parse JSON file
    const jsonData = JSON.parse(fs.readFileSync(filePath, "utf8"));

    // Check for duplicate keys
    const keysSet = new Set();
    const duplicateKeys = [];

    for (const key in jsonData) {
        if (keysSet.has(key)) {
            duplicateKeys.push(key);
        }
        keysSet.add(key);
    }

    // Log duplicates if found
    if (duplicateKeys.length > 0) {
        console.warn("⚠️ Warning: Duplicate keys found:", duplicateKeys);
    } else {
        console.log("✅ No duplicate keys found.");
    }

    // Convert JSON to CSV format
    const csvContent = Object.entries(jsonData)
        .map(([key, value]) => `"${key}","${value}",""`) // Third column left empty
        .join("\n");

    // Add CSV header
    const csvHeader = `"Key","English Value","Chinese Value"\n`;
    const csvFinal = csvHeader + csvContent;

    // Save CSV to file
    const csvFilePath = path.join(__dirname, "translations", `${fileName}.csv`);
    fs.writeFileSync(csvFilePath, csvFinal, "utf8");

    console.log("✅ CSV file has been created: translations.csv");

} catch (error) {
    console.error("❌ Error processing file:", error);
}
