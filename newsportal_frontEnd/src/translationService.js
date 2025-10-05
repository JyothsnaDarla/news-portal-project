// --- CONFIGURATION (Use the exact URL and Key) ---
const API_URL = "http://localhost:8001/translate";
const API_KEY = "translate_to_hindi_Coderbot"; // Use the exact key you verified!

export async function translateToHindi(englishText) {
    
    const requestBody = {
        text: englishText,
    };

    try {
        // Send the POST request to your local API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': API_KEY 
            },
            body: JSON.stringify(requestBody)
        });

        if (!response.ok) {
            // Handle errors (e.g., if the API is down)
            throw new Error(`Translation API failed with status: ${response.status}`);
        }

        const data = await response.json();
        return data.translation;

    } catch (error) {
        console.error("Translation API Error:", error);
        return englishText; // Fallback: Return original English text
    }
}

// --- Example of usage in a React component (e.g., NewsCard.js) ---
// import { translateToHindi } from './translationService';
// 
// // Inside a React component:
// const [hindiTitle, setHindiTitle] = useState('Loading...');
// 
// useEffect(() => {
//   translateToHindi(props.newsItem.title).then(setHindiTitle);
// }, [props.newsItem.title]);
// 
// // Render: <h1>{hindiTitle}</h1>