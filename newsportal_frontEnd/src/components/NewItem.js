// newsportal_frontEnd/src/components/NewsItem.js

import React, { useState, useEffect } from 'react';
// Import the service you created in translationService.js
import { translateToHindi } from '../translationService'; 

function NewsItem({ item }) {
    // 1. Create state to hold the translated title
    const [hindiTitle, setHindiTitle] = useState(item.title);

    useEffect(() => {
        // 2. Check if translation is needed (e.g., based on a user language setting)
        const isHindiMode = true; // Replace with your actual language setting check

        if (isHindiMode) {
            // 3. Call the async function and update state when it resolves
            translateToHindi(item.title)
                .then(setHindiTitle)
                .catch(error => console.error("Failed to display Hindi title", error));
        } else {
            // Fallback to original title
            setHindiTitle(item.title);
        }
    }, [item.title]); // Re-run effect if the item title changes

    return (
        <div className="news-card">
            {/* 4. Display the state variable */}
            <h2>{hindiTitle}</h2>
            <p>{item.summary}</p> 
            {/* You would repeat the useEffect logic for the summary/content too */}
        </div>
    );
}

export default NewsItem;