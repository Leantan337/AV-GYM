/**
 * Manual Translation Feature
 * 
 * This script enables the translation button functionality on pages.
 * When the translate button is clicked, it looks up text in the manual translation dictionary
 * and replaces content on the page with translated versions.
 */

class ManualTranslator {
    constructor(options = {}) {
        this.options = Object.assign({
            apiEndpoint: '/translation/api/translate/',
            sourceLanguage: 'en',
            targetLanguage: 'es',
            selectors: ['.translatable', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', '.btn', '.nav-link'],
            excludeSelectors: ['.no-translate', 'code', 'pre', 'script', 'style'],
            buttonText: 'Translate',
            buttonOriginalText: 'Original',
            buttonPosition: 'top-right',
        }, options);
        
        this.isTranslated = false;
        this.originalContent = new Map();
        this.translationCache = new Map();
        
        this.init();
    }
    
    init() {
        this.createButton();
        this.attachEventListeners();
    }
    
    createButton() {
        // Create the translation button
        this.button = document.createElement('button');
        this.button.classList.add('translation-button');
        this.button.textContent = this.options.buttonText;
        this.button.style.position = 'fixed';
        this.button.style.zIndex = '9999';
        this.button.style.padding = '10px 15px';
        this.button.style.borderRadius = '4px';
        this.button.style.backgroundColor = '#0d6efd';
        this.button.style.color = 'white';
        this.button.style.border = 'none';
        this.button.style.boxShadow = '0 2px 5px rgba(0,0,0,0.2)';
        this.button.style.cursor = 'pointer';
        
        // Position the button
        switch (this.options.buttonPosition) {
            case 'top-right':
                this.button.style.top = '20px';
                this.button.style.right = '20px';
                break;
            case 'top-left':
                this.button.style.top = '20px';
                this.button.style.left = '20px';
                break;
            case 'bottom-right':
                this.button.style.bottom = '20px';
                this.button.style.right = '20px';
                break;
            case 'bottom-left':
                this.button.style.bottom = '20px';
                this.button.style.left = '20px';
                break;
            default:
                this.button.style.top = '20px';
                this.button.style.right = '20px';
        }
        
        document.body.appendChild(this.button);
    }
    
    attachEventListeners() {
        this.button.addEventListener('click', () => {
            if (this.isTranslated) {
                this.restoreOriginalContent();
                this.button.textContent = this.options.buttonText;
                this.isTranslated = false;
            } else {
                this.translatePage();
                this.button.textContent = this.options.buttonOriginalText;
                this.isTranslated = true;
            }
        });
    }
    
    async translatePage() {
        // Get all elements to translate
        const elements = this.getTranslatableElements();
        
        // Store original content for later restoration
        elements.forEach(element => {
            if (!this.originalContent.has(element)) {
                this.originalContent.set(element, element.textContent);
            }
        });
        
        // Translate each element
        for (const element of elements) {
            const originalText = this.originalContent.get(element);
            
            // Skip empty text or very short text
            if (!originalText || originalText.trim().length < 2) {
                continue;
            }
            
            // Check if translation is already in cache
            if (this.translationCache.has(originalText)) {
                element.textContent = this.translationCache.get(originalText);
                continue;
            }
            
            // Call the translation API
            try {
                const translatedText = await this.translateText(originalText);
                element.textContent = translatedText;
                this.translationCache.set(originalText, translatedText);
            } catch (error) {
                console.error('Translation error:', error);
            }
        }
    }
    
    restoreOriginalContent() {
        this.originalContent.forEach((originalText, element) => {
            element.textContent = originalText;
        });
    }
    
    getTranslatableElements() {
        const allElements = [];
        
        // Add elements with specified selectors
        this.options.selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                // Check if the element should be excluded
                let shouldExclude = false;
                this.options.excludeSelectors.forEach(excludeSelector => {
                    if (element.matches(excludeSelector) || 
                        element.closest(excludeSelector)) {
                        shouldExclude = true;
                    }
                });
                
                if (!shouldExclude) {
                    allElements.push(element);
                }
            });
        });
        
        return allElements;
    }
    
    async translateText(text) {
        try {
            const response = await fetch(this.options.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({
                    text: text,
                    source_language: this.options.sourceLanguage,
                    target_language: this.options.targetLanguage,
                }),
            });
            
            if (!response.ok) {
                throw new Error('Translation API error');
            }
            
            const data = await response.json();
            return data.translated_text;
        } catch (error) {
            console.error('Translation API error:', error);
            return text; // Return original text if translation fails
        }
    }
    
    getCsrfToken() {
        // Get CSRF token from cookie or meta tag
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
            
        if (cookieValue) {
            return cookieValue;
        }
        
        // Try to get from meta tag
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        return metaTag ? metaTag.getAttribute('content') : '';
    }
}

// Helper function to initialize the translator
function initTranslator(options = {}) {
    document.addEventListener('DOMContentLoaded', () => {
        window.translator = new ManualTranslator(options);
    });
}
