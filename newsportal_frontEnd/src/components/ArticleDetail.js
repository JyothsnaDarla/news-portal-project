import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { format } from 'date-fns'; 
import api from '../api';
import CommentForm from './commentForm'; 

// FIX: DATE PARSING HELPER FUNCTION (Handles various date string formats)
const safeParseDate = (isoString) => {
    if (!isoString) return new Date(); 
    
    // Simplifies the string by removing fractional seconds and timezone
    const simplifiedString = isoString.substring(0, 19).replace('T', ' '); 
    
    const date = new Date(simplifiedString);
    
    if (isNaN(date.getTime())) {
        return new Date(isoString); 
    }
    return date;
};

function ArticleDetail() {
    const { id } = useParams(); 
    const [article, setArticle] = useState(null);
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchArticleData = useCallback(() => {
        setLoading(true);
        // 1. Fetch Comments
        api.get(`articles/${id}/comments/`) 
            .then(response => {
                setComments(response.data); 
                // 2. Fetch Article Details
                return api.get(`articles/${id}/`);
            })
            .then(response => {
                setArticle(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setLoading(false);
            });
    }, [id]);

    useEffect(() => {
        fetchArticleData();
    }, [fetchArticleData]);

    if (loading) {
        return <div className="loading">लेख लोड हो रहा है...</div>;
    }

    if (!article) {
        return <div className="error">लेख नहीं मिला</div>;
    }

    return (
        <div className="article-detail">
            <h1>{article.title}</h1>
            <p className="category-info">
                श्रेणी:**{article.category ? article.category.name : 'N/A'}** |प्रकाशित: {article.publication_date
                    ? format(safeParseDate(article.publication_date), 'dd MMMM yyyy, hh:mm a') 
                    : 'N/A Time'}
            </p>
            
            {/* CORRECTED MEDIA RENDERING LOGIC (Stacked with full URL) */}
            <div className="article-media">
                
                {/* Display all Images */}
                {article.images && article.images.length > 0 && 
                    article.images.map(image => (
                        <img 
                            key={image.id}
                            src={`http://localhost:8000${image.image_file}`} 
                            alt={article.title} 
                            className="main-image" 
                            style={{ marginBottom: '15px' }}
                        />
                    ))
                }
                
                {/* Display all Videos */}
                {article.videos && article.videos.length > 0 && 
                    article.videos.map(video => (
                        <video 
                            key={video.id}
                            src={`http://localhost:8000${video.video_file}`} 
                            controls 
                            className="main-video"
                            style={{ marginBottom: '15px' }}
                        >
                            आपका ब्राउज़र इस वीडियो टैग का समर्थन नहीं करता है।
                        </video>
                    ))
                }

                {/* Fallback if no media exists */}
                {(!article.images || article.images.length === 0) && 
                 (!article.videos || article.videos.length === 0) && (
                    <div className="no-media-placeholder">कोई मीडिया नहीं</div>
                )}
            </div>
            
            {/* 🚨 FIX: DISPLAY BOTH SHORT AND LONG DESCRIPTIONS 🚨 */}
            <div className="article-content">
                {/* 1. Short Description (Using the likely API field name: short_description) */}
                {article.short_description && (
                    <p className="short-description" style={{fontWeight: 'bold', fontSize: '1.2em', marginBottom: '1em'}}>
                        {article.short_description}
                    </p>
                )}
                
                {/* 2. Detailed/Long Description (Main body content) */}
                {article.detailed_description && (
                    <p className="long-description">
                        {article.detailed_description}
                    </p>
                )}

                {/* Fallback if ALL content fields are empty */}
                {(!article.short_description && !article.detailed_description) && (
                    <p>लेख की सामग्री उपलब्ध नहीं है.</p>
                )}
            </div>

            <hr />

            <div className="comments-section">
                <h2>टिप्पणियाँ ({comments.length})</h2>
                
                <CommentForm articleId={id} onCommentSubmitted={fetchArticleData} /> 

                <div className="comment-list">
                    {comments.length > 0 ? (
                        comments.map(comment => (
                            <div key={comment.id} className="comment-item">
                                <p className="comment-body">{comment.content}</p> 
                                <small>
                                    द्वारा: **{comment.author_name || 'Anonymous'}** चालू {format(new Date(comment.created_at),'dd MMM yyyy,hh:mm a')}
                                </small>
                            </div>
                        ))
                    ) : (
                        <p>सबसे पहले टिप्पणी करें!</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ArticleDetail;