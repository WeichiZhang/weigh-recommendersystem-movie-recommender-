// enhanced-two-tower.js - FIXED VERSION
class EnhancedTwoTower {
    constructor() {
        this.movieData = [];
        this.llmFeatures = {};
        this.initialized = false;
        this.sampleMovies = this.createSampleMovies();
    }

    createSampleMovies() {
        return [
            { id: 1, title: "When Harry Met Sally", year: 1989, genres: ["comedy", "romance"], overview: "A man and a woman struggle to be friends without sex getting in the way." },
            { id: 2, title: "Pretty Woman", year: 1990, genres: ["romance", "comedy"], overview: "A man falls in love with a prostitute he hires to be his escort for business functions." },
            { id: 3, title: "10 Things I Hate About You", year: 1999, genres: ["comedy", "romance"], overview: "A new student must find a guy to date the meanest girl in school." },
            { id: 4, title: "The Notebook", year: 2004, genres: ["romance", "drama"], overview: "A poor young man falls in love with a rich young woman." },
            { id: 5, title: "Crazy Rich Asians", year: 2018, genres: ["comedy", "romance"], overview: "A native New Yorker Rachel Chu accompanies her boyfriend to Singapore." },
            { id: 6, title: "La La Land", year: 2016, genres: ["romance", "drama", "musical"], overview: "A jazz pianist falls for an aspiring actress in Los Angeles." },
            { id: 7, title: "The Silence of the Lambs", year: 1991, genres: ["thriller", "drama"], overview: "A young FBI cadet must confide in an incarcerated manipulative killer." },
            { id: 8, title: "Se7en", year: 1995, genres: ["thriller", "crime"], overview: "Two detectives hunt a serial killer who uses the seven deadly sins as his motives." },
            { id: 9, title: "The Dark Knight", year: 2008, genres: ["action", "thriller"], overview: "Batman faces the Joker, a criminal mastermind who seeks to undermine society." },
            { id: 10, title: "Inception", year: 2010, genres: ["action", "sci-fi"], overview: "A thief who steals corporate secrets through dream-sharing technology." }
        ];
    }

    async initialize() {
        if (this.initialized) return;
        
        try {
            await this.generateLLMFeatures();
            this.initialized = true;
            console.log("Enhanced Two-Tower with LLM features initialized");
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    async generateLLMFeatures() {
        // Generate LLM features for each movie
        for (const movie of this.sampleMovies) {
            this.llmFeatures[movie.id] = this.extractLLMFeatures(movie);
        }
    }

    extractLLMFeatures(movie) {
        const title = movie.title.toLowerCase();
        const overview = movie.overview.toLowerCase();
        const text = title + ' ' + overview;
        
        return {
            genres: movie.genres,
            themes: this.extractThemes(text, movie.genres),
            tone: this.analyzeTone(text),
            target_audience: this.determineAudience(movie.genres)
        };
    }

    extractThemes(text, genres) {
        const themes = [];
        
        if (text.includes('love') || text.includes('romance') || genres.includes('romance')) {
            themes.push('romance');
        }
        if (text.includes('friend') || text.includes('buddy')) {
            themes.push('friendship');
        }
        if (text.includes('family') || text.includes('parent')) {
            themes.push('family');
        }
        if (text.includes('comedy') || text.includes('funny') || text.includes('humor')) {
            themes.push('comedy');
        }
        if (text.includes('crime') || text.includes('detective') || text.includes('murder')) {
            themes.push('crime');
        }
        if (text.includes('action') || text.includes('adventure') || text.includes('fight')) {
            themes.push('action');
        }

        return themes.length > 0 ? themes : ['human experience'];
    }

    analyzeTone(text) {
        if (text.includes('dark') || text.includes('grim') || text.includes('murder')) {
            return 'dark';
        } else if (text.includes('funny') || text.includes('comedy') || text.includes('light')) {
            return 'lighthearted';
        } else if (text.includes('romance') || text.includes('love')) {
            return 'romantic';
        } else if (text.includes('suspense') || text.includes('thriller')) {
            return 'suspenseful';
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

    // FIXED: Actually process the user query
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
        }
        
        if (queryLower.includes('thriller') || queryLower.includes('suspense')) {
            intent = "thriller";
            preferredGenres.push('thriller');
            preferredTone = 'suspenseful';
        }
        
        if (queryLower.includes('drama')) {
            intent = "drama";
            preferredGenres.push('drama');
        }

        // Extract exclusions
        if (queryLower.includes('no horror') || queryLower.includes('not scary')) {
            excludedGenres.push('horror');
        }
        if (queryLower.includes('no action')) {
            excludedGenres.push('action');
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
        const recommendations = this.sampleMovies.map(movie => {
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
        
        return {
            recommendations: filteredRecs,
            searchCriteria: searchCriteria
        };
    }

    // Traditional method (your existing functionality)
    async getTraditionalRecommendations(userId, topK = 10) {
        await this.initialize();
        
        // Simulate traditional recommendations
        const shuffled = [...this.sampleMovies].sort(() => 0.5 - Math.random());
        return shuffled.slice(0, topK).map((movie, index) => ({
            id: movie.id,
            title: movie.title,
            score: (topK - index) * 0.1,
            year: movie.year
        }));
    }
}

// Initialize global instance
window.EnhancedTwoTower = new EnhancedTwoTower();
