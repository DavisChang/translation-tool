const fs = require('fs');

/**
 * Reads and sorts a JSON file alphabetically.
 * @param {string} filePath - The path to the translation JSON file.
 * @returns {object} - The sorted JSON object.
 */
function readAndSortJson(filePath) {
    const rawData = fs.readFileSync(filePath, 'utf8');
    const jsonData = JSON.parse(rawData);
    
    // Recursively sort the JSON object keys alphabetically
    function sortObject(obj) {
        return Object.keys(obj).sort().reduce((acc, key) => {
            acc[key] = typeof obj[key] === 'object' ? sortObject(obj[key]) : obj[key];
            return acc;
        }, {});
    }

    return sortObject(jsonData);
}

/**
 * Checks if the target translation file has all the keys from the base language.
 * @param {string} baseLang - The reference language (usually "en").
 * @param {string} targetLang - The target language to validate (e.g., "zh").
 */
function checkTranslations(baseLang, targetLang) {
    const basePath = `locales/${baseLang}.json`;
    const targetPath = `locales/${targetLang}.json`;

    const baseData = readAndSortJson(basePath);
    const targetData = readAndSortJson(targetPath);

    const missingKeys = [];

    function compareKeys(baseObj, targetObj, parentKey = '') {
        Object.keys(baseObj).forEach(key => {
            const fullKey = parentKey ? `${parentKey}.${key}` : key;
            if (!(key in targetObj)) {
                missingKeys.push(fullKey);
            } else if (typeof baseObj[key] === 'object' && typeof targetObj[key] === 'object') {
                compareKeys(baseObj[key], targetObj[key], fullKey);
            }
        });
    }

    compareKeys(baseData, targetData);

    if (missingKeys.length > 0) {
        console.log(`❌ ${targetLang}.json is missing the following keys:`);
        missingKeys.forEach(key => console.log(`   - ${key}`));
        process.exit(1); // Fail CI/CD if keys are missing
    } else {
        console.log(`✅ ${targetLang}.json is complete.`);
    }

    // Automatically sort and overwrite the JSON files
    fs.writeFileSync(basePath, JSON.stringify(baseData, null, 2) + "\n", 'utf8');
    fs.writeFileSync(targetPath, JSON.stringify(targetData, null, 2) + "\n", 'utf8');

    console.log(`🔄 Successfully sorted ${baseLang}.json and ${targetLang}.json.`);
}

// **Supports multiple language checks**
const languages = ["zh"]; // Add other languages like "ja", "fr" if needed
languages.forEach(lang => checkTranslations("en", lang));
