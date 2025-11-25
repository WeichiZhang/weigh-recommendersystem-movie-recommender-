// two-tower.js - FIXED VERSION WITH SAMPLE DATA
class EnhancedTwoTower {
    constructor() {
        this.movieData = this.createSampleMovies();
        this.llmFeatures = {};
        this.initialized = false;
        console.log("Enhanced Two-Tower initialized with sample data");
    }

    createSampleMovies() {
        return [
            { id: 1, title: "When Harry Met Sally", year: 1989, genres: ["comedy", "romance"] },
            { id: 2, title: "Pretty Woman", year: 1990, genres: ["romance", "comedy"] },
            { id: 3, title: "10 Things I Hate About You", year: 1999, genres: ["comedy", "romance"] },
            { id: 4, title: "The Notebook", year: 2004, genres: ["romance", "drama"] },
            { id: 5, title: "Crazy Rich Asians", year: 2018, genres: ["comedy", "romance"] },
            { id: 6, title: "La La Land", year: 2016, genres: ["romance", "drama", "musical"] },
            { id: 7, title: "The Silence of the Lambs", year: 1991, genres: ["thriller", "drama"] },
            { id: 8, title: "Se7en", year: 1995, genres: ["thriller", "crime"] },
            { id: 9, title: "The Dark Knight", year: 2008, genres: ["action", "thriller"] },
            { id: 10, title: "Inception", year: 2010, genres: ["action", "sci-fi"] },
            { id: 11, title: "The Shawshank Redemption", year: 1994, genres: ["drama"] },
            { id: 12, title: "Pulp Fiction", year: 1994, genres: ["crime", "drama"] },
            { id: 13, title: "Forrest Gump", year: 1994, genres: ["drama", "romance"] },
            { id: 14, title: "The Godfather", year: 1972, genres: ["crime", "drama"] },
            { id: 15, title: "The Matrix", year: 1999, genres: ["action", "sci-fi"] }
        ];
    }

    async initialize() {
        if (this.initialized) return;
        
        try {
            await this.generateLLMFeatures();
            this.initialized = true;
            console.log("Enhanced Two-Tower with LLM features ready");
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    async generateLLMFeatures() {
        // Generate LLM features for each movie
        for (const movie of this.movieData) {
            this.llmFeatures[movie.id] = this.extractLLMFeatures(movie);
        }
    }

    extractLLMFeatures(movie) {
        const title = movie.title.toLowerCase();
        const genres = movie.genres || [];
        
        return {
            genres: genres,
            themes: this.extractThemes(title, genres),
            tone: this.analyzeTone(title, genres),
            target_audience: this.determineAudience(genres)
        };
    }

    extractThemes(title, genres) {
        const themes = [];
        
        if (title.includes('love') || title.includes('romance') || genres.includes('romance')) {
            themes.push('romance');
        }
        if (title.includes('friend') || title.includes('buddy')) {
            themes.push('friendship');
        }
        if (title.includes('family') || title.includes('parent')) {
            themes.push('family');
        }
        if (title.includes('comedy') || title.includes('funny') || genres.includes('comedy')) {
            themes.push('comedy');
        }
        if (title.includes('crime') || title.includes('detective') || title.includes('murder')) {
            themes.push('crime');
        }
        if (title.includes('action') || title.includes('adventure') || title.includes('fight')) {
            themes.push('action');
        }
        if (title.includes('sci-fi') || title.includes('future') || title.includes('space')) {
            themes.push('science fiction');
        }

        return themes.length > 0 ? themes : ['human experience'];
    }

    analyzeTone(title, genres) {
        if (title.includes('dark') || title.includes('grim') || title.includes('murder')) {
            return 'dark';
        } else if (title.includes('funny') || title.includes('comedy') || title.includes('light')) {
            return 'lighthearted';
        } else if (title.includes('romance') || title.includes('love')) {
            return 'romantic';
        } else if (title.includes('suspense') || title.includes('thriller')) {
            return 'suspenseful';
        } else if (genres.includes('action')) {
            return 'exciting';
        } else {
            return 'neutral';
        }
    }

    determineAudience(genres) {
        if (genres.includes('horror') || genres.includes('thriller')) {
            return 'adult';
        } else if (genres.includes('comedy') || genres.includes('romance')) {
            return 'teen-adult';
        } else {
            return 'general';
        }
    }

    // ACTUALLY process the user query
    processUserQuery(query) {
        const queryLower = query.toLowerCase();
        
        let intent = "general";
        let preferredGenres = [];
        let excludedGenres = [];
        let preferredThemes = [];
        let preferredTone = "neutral";

        // Analyze query for intent
        if (queryLower.includes('romantic') || queryLower.includes('romance') || queryLower.includes('love')) {
            intent = "romance";
            preferredGenres.push('romance');
            preferredThemes.push('romance');
            preferredTone = 'romantic';
        }
        
        if (queryLower.includes('comedy') || queryLower.includes('funny') || queryLower.includes('humor')) {
            intent = intent === "romance" ? "romantic comedy" : "comedy";
            preferredGenres.push('comedy');
            preferredThemes.push('comedy');
            preferredTone = 'lighthearted';
        }
        
        if (queryLower.includes('action') || queryLower.includes('adventure')) {
            intent = "action";
            preferredGenres.push('action');
            preferredThemes.push('action');
            preferredTone = 'exciting';
        }
        
        if (queryLower.includes('thriller') || queryLower.includes('suspense') || queryLower.includes('mystery')) {
            intent = "thriller";
            preferredGenres.push('thriller');
            preferredTone = 'suspenseful';
        }
        
        if (queryLower.includes('drama')) {
            intent = "drama";
            preferredGenres.push('drama');
        }

        if (queryLower.includes('sci-fi') || queryLower.includes('science fiction')) {
            intent = "sci-fi";
            preferredGenres.push('sci-fi');
            preferredThemes.push('science fiction');
        }

        // Extract exclusions
        if (queryLower.includes('no horror') || queryLower.includes('not scary')) {
            excludedGenres.push('horror');
        }
        if (queryLower.includes('no action')) {
            excludedGenres.push('action');
        }
        if (queryLower.includes('no comedy')) {
            excludedGenres.push('comedy');
        }

        // Remove duplicates
        preferredGenres = [...new Set(preferredGenres)];
        preferredThemes = [...new Set(preferredThemes)];

        // If no specific intent detected, use general
        if (intent === "general") {
            preferredGenres = ['drama', 'comedy']; // Default fallback
        }

        return {
            original_query: query,
            intent: intent,
            preferred_genres: preferredGenres,
            excluded_genres: excludedGenres,
            preferred_themes: preferredThemes,
            preferred_tone: preferredTone
        };
    }

    calculateMatchScore(movie, searchCriteria) {
        let score = 0;
        const llmFeatures = this.llmFeatures[movie.id];
        
        // Genre matching (most important)
        const genreMatches = llmFeatures.genres.filter(genre => 
            searchCriteria.preferred_genres.includes(genre)
        );
        score += genreMatches.length * 0.4;
        
        // Theme matching
        const themeMatches = llmFeatures.themes.filter(theme =>
            searchCriteria.preferred_themes.includes(theme)
        );
        score += themeMatches.length * 0.3;
        
        // Tone matching
        if (llmFeatures.tone === searchCriteria.preferred_tone) {
            score += 0.2;
        }
        
        // Penalty for excluded genres
        const hasExcludedGenre = llmFeatures.genres.some(genre =>
            searchCriteria.excluded_genres.includes(genre)
        );
        if (hasExcludedGenre) {
            score *= 0.1; // Heavy penalty
        }
        
        // Add some randomness for variety
        score += Math.random() * 0.1;
        
        return Math.min(score, 1.0); // Cap at 1.0
    }

    generateExplanation(movieTitle, searchCriteria, llmFeatures) {
        const reasons = [];
        
        // Check genre matches
        const matchingGenres = searchCriteria.preferred_genres.filter(genre =>
            llmFeatures.genres.includes(genre)
        );
        if (matchingGenres.length > 0) {
            reasons.push(`${matchingGenres.join(', ')} elements`);
        }
        
        // Check theme matches
        const matchingThemes = searchCriteria.preferred_themes.filter(theme =>
            llmFeatures.themes.includes(theme)
        );
        if (matchingThemes.length > 0) {
            reasons.push(`${matchingThemes.join(', ')} themes`);
        }
        
        // Check tone matches
        if (llmFeatures.tone === searchCriteria.preferred_tone && searchCriteria.preferred_tone !== 'neutral') {
            reasons.push(`${llmFeatures.tone} atmosphere`);
        }
        
        if (reasons.length > 0) {
            return `Matches your interest in ${reasons.join(' and ')}`;
        } else {
            return 'High-quality content that aligns with general preferences';
        }
    }

    async getEnhancedRecommendations(userQuery, topK = 10) {
        await this.initialize();
        
        // ACTUALLY process the user query
        const searchCriteria = this.processUserQuery(userQuery);
        
        // Calculate recommendations based on actual matching
        const recommendations = this.movieData.map(movie => {
            const llmFeatures = this.llmFeatures[movie.id];
            const score = this.calculateMatchScore(movie, searchCriteria);
            const explanation = this.generateExplanation(movie.title, searchCriteria, llmFeatures);
            
            return {
                id: movie.id,
                title: movie.title,
                score: score,
                llm_genres: llmFeatures.genres,
                llm_themes: llmFeatures.themes,
                llm_tone: llmFeatures.tone,
                explanation: explanation,
                year: movie.year
            };
        });
        
        // Filter out very low scores and sort
        const filteredRecs = recommendations
            .filter(rec => rec.score > 0.1)
            .sort((a, b) => b.score - a.score)
            .slice(0, topK);
        
        return filteredRecs;
    }

    // Traditional method for user ID based recommendations
    async getTraditionalRecommendations(userId, topK = 10) {
        await this.initialize();
        
        // For demo purposes, return some sample recommendations
        // In a real system, this would use actual user embeddings
        const shuffled = [...this.movieData].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, topK).map((movie, index) => ({
            id: movie.id,
            title: movie.title,
            score: (topK - index) * 0.1 + Math.random() * 0.1,
            year: movie.year
        }));
    }
}

// Initialize global instance
window.EnhancedTwoTower = new EnhancedTwoTower();
