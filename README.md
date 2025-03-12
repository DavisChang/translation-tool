# How to Use the Multi-Language Translation Management System
This project provides a complete multi-language translation workflow, supporting Web (React), Android, and Windows (WPF). It ensures all translation files remain synchronized and consistent, without relying on external translation services.


## Project Structure

```
/locales
  ├── en.json               # English translations (source language)
  ├── zh.json               # Traditional Chinese translations
  ├── android/
      ├── strings_en.xml    # Android English translations (auto-generated)
      ├── strings_zh.xml    # Android Chinese translations (auto-generated)
  ├── windows/
      ├── resx_en.resx      # Windows English translations (auto-generated)
      ├── resx_zh.resx      # Windows Chinese translations (auto-generated)
  ├── web/
      ├── en_web.json       # Web English translations (auto-generated)
      ├── zh_web.json       # Web Chinese translations (auto-generated)
/scripts
  ├── convert.py            # Python script: Converts JSON to Android XML / Windows RESX
  ├── validate-i18n.js      # Node.js script: Validates translation completeness
```

## Add HTML via a Helper Function in React

1. Keep en.json Plain
```json
{
  "auth": {
    "login": {
      "button": "Sign In",
      "forgot_password": "Forgot your password?"
    }
  }
}
```

2. Step 2: Add HTML via a Helper Function in React

```tsx
const formatHTML = (textKey: string) => {
  const { t } = useTranslation();
  let text = t(textKey);

  const formatMap: Record<string, (text: string) => string> = {
    "auth.login.forgot_password": (text) =>
      `<a href='/forgot-password' class='text-blue-500 hover:underline'>${text}</a>`,
    "auth.login.button": (text) =>
      `<button class='btn-primary'>${text}</button>`
  };

  return formatMap[textKey] ? formatMap[textKey](text) : text;
};

const Login = () => {
  return (
    <div>
      <div dangerouslySetInnerHTML={{ __html: formatHTML("auth.login.forgot_password") }} />
      <div dangerouslySetInnerHTML={{ __html: formatHTML("auth.login.button") }} />
    </div>
  );
};
```

Why is this better?
✅ Keeps en.json clean.
✅ No issues for Android, iOS, and Windows clients.
✅ Web gets full HTML styling.

## How to Add or Modify Translations

1. Modify /locales/en.json (source language JSON)
2. Update /locales/zh.json, /locales/ja.json, /locales/fr.json accordingly
3. Run convert.py to generate translations for Android and Windows
4. Run validate-i18n.js to ensure completeness
5. Submit a PR and ensure CI/CD passes


### Example Update
If you need to add a "Logout" button translation:

/locales/en.json
```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel",
    "logout": "Logout"  // New key
  }
}
```

/locales/zh.json
```json
{
  "common": {
    "save": "儲存",
    "cancel": "取消",
    "logout": "登出"  // New key
  }
}
```
Ensure all languages contain the same keys to prevent missing translations!


## Validate Translation Completeness

Run the following command:

```shell
node scripts/validate-i18n.js
```

If a translation is missing, you will see an error message:

❌ zh.json is missing the following keys:
   - common.logout
  
📌 If all translations are complete, you will see:

✅ zh.json is complete
🔄 en.json and zh.json have been auto-sorted

## Convert JSON to Android / Windows Format

Run the following command:

```shell
python scripts/convert.py
```

This will generate:

- /locales/android/strings_en.xml
- /locales/android/strings_zh.xml
- /locales/windows/resx_en.resx
- /locales/windows/resx_zh.resx


## How to Add a New Language
Example: Adding Spanish (es.json)


Copy en.json as a template

```sh
cp locales/en.json locales/es.json
```

Manually translate locales/es.json

```json
{
  "common": {
    "save": "Guardar",
    "cancel": "Cancelar",
    "logout": "Cerrar sesión"
  }
}
```

Update /scripts/validate-i18n.js to include "es" in the languages array:

```js
const languages = ["zh", "es"]; // Added Spanish
```

Generate translations for Android and Windows

```shell
python scripts/convert.py
```

Run translation validation

```shell
node scripts/validate-i18n.js
```

## CI/CD Automation
This project uses GitHub Actions to automatically check JSON translation completeness whenever a PR is created:

```yaml
name: Validate Translations

on:
  pull_request:
    branches:
      - main

jobs:
  validate-i18n:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v3

      - name: Install Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Run translation validation
        run: node scripts/validate-i18n.js
```

 If any translation key is missing, the PR will automatically fail, preventing incomplete translations from being merged!


## Best Practices for Designing and Maintaining en.json

### 1. Use a Consistent Hierarchical Structure
- Group translations by feature or context (e.g., auth, dashboard, settings).
- Avoid mixing different types of translations in the same level.

```json
{
  "common": {
    "save": "Save"
  },
  "navigation": {
    "home": "Home"
  },
  "auth": {
    "login": {
      "title": "Login"
    }
  },
  "errors": {
    "network": "Network error"
  }
}
```

### 2. Keep Key Names Short, but Meaningful
- Avoid unnecessary words like label_, text_, or msg_.
- Use descriptive yet short keys.

```json
{
  "auth": {
    "login": {
      "button": "Sign In",
      "placeholder_username": "Enter your username"
    }
  }
}
```

### 3. Use Placeholders for Dynamic Values
For texts containing user-specific data, use {variable_name} placeholders.

```json
{
  "dashboard": {
    "welcome_message": "Welcome back, {name}!"
  }
}

```

```tsx
const { t } = useTranslation();
const username = "John";
return <h1>{t("dashboard.welcome_message", { name: username })}</h1>;
```

### 4. Standardize Naming Conventions
   
**Standardize Naming Conventions**

| **Type**             | **Naming Convention**        | **Example**                      |
|----------------------|----------------------------|----------------------------------|
| **Common Actions**   | `common.action_name`       | `common.save`, `common.cancel`  |
| **Navigation Items** | `navigation.page_name`     | `navigation.home`, `navigation.settings` |
| **Authentication**   | `auth.[login/signup/logout]` | `auth.login.title`, `auth.signup.button` |
| **Errors**          | `errors.error_type`         | `errors.network`, `errors.server` |
| **Forms**           | `form.field_name`           | `form.required`, `form.invalid_email` |


Avoid Duplicating Translations
Instead of writing the same translation in multiple places, reference common keys.

```json
{
  "common": {
    "login": "Login"
  },
  "auth": {
    "login": {
      "button": "{common.login}"
    }
  },
  "dashboard": {
    "action_login": "{common.login}"
  }
}
```

If using i18next, use t("common.login") to reference the common translation.
