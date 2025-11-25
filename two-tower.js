// enhanced-two-tower.js
class EnhancedTwoTower {
    constructor() {
        this.userEmbeddings = null;
        this.itemEmbeddings = null;
        this.movieData = null;
        this.llmFeatures = {};
        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) return;
        
        try {
            // Load your existing embeddings and data
            await this.loadModelData();
            await this.generateLLMFeatures();
            this.initialized = true;
            console.log("Enhanced Two-Tower with LLM features initialized");
        } catch (error) {
            console.error("Initialization failed:", error);
        }
    }

    async loadModelData() {
        // Load your existing user and item embeddings
        // This should match your current data loading logic
        const response = await fetch('data/embeddings.json');
        const data = await response.json();
        this.userEmbeddings = data.userEmbeddings;
        this.itemEmbeddings = data.itemEmbeddings;
        this.movieData = data.movies;
    }

    async generateLLMFeatures() {
        // Generate LLM features for each movie
        for (const movie of this.movieData) {
            this.llmFeatures[movie.id] = this.extractLLMFeatures(movie);
        }
    }

    extractLLMFeatures(movie) {
        // Simulate LLM feature extraction based on movie title and genres
        const title = movie.title.toLowerCase();
        const genres = movie.genres ? movie.genres.toLowerCase() : '';
        
        // Genre detection
        const detectedGenres = this.detectGenres(title + ' ' + genres);
        
        // Theme extraction
        const themes = this.extractThemes(title);
        
        // Tone analysis
        const tone = this.analyzeTone(title);
        
        return {
            genres: detectedGenres,
            themes: themes,
            tone: tone,
            target_audience: this.determineAudience(detectedGenres)
        };
    }

    detectGenres(text) {
        const genres = [];
        const genreKeywords = {
            'action': ['action', 'adventure', 'fight', 'battle', 'mission'],
            'comedy': ['comedy', 'funny', 'humor', 'laugh'],
            'drama': ['drama', 'emotional', 'relationship', 'family'],
            'thriller': ['thriller', 'suspense', 'mystery', 'crime'],
            'sci-fi': ['sci-fi', 'science fiction', 'space', 'alien', 'future'],
            'romance': ['romance', 'love', 'relationship'],
            'horror': ['horror', 'scary', 'terror', 'fear'],
            'documentary': ['documentary', 'real story', 'biography']
        };

        for (const [genre, keywords] of Object.entries(genreKeywords)) {
            if (keywords.some(keyword => text.includes(keyword))) {
                genres.push(genre);
            }
        }

        return genres.length > 0 ? genres : ['drama'];
    }

    extractThemes(title) {
        const themes = [];
        const themeKeywords = {
            'friendship': ['friend', 'buddy', 'companion'],
            'love': ['love', 'romance', 'relationship'],
            'betrayal': ['betray', 'treason', 'deception'],
            'revenge': ['revenge', 'vengeance'],
            'justice': ['justice', 'law', 'court'],
            'survival': ['survive', 'survival'],
            'identity': ['identity', 'self-discovery'],
            'technology': ['technology', 'computer', 'AI', 'robot']
        };

        for (const [theme, keywords] of Object.entries(themeKeywords)) {
            if (keywords.some(keyword => title.includes(keyword))) {
                themes.push(theme);
            }
        }

        return themes.length > 0 ? themes : ['human experience'];
    }

    analyzeTone(title) {
        const toneIndicators = {
            'dark': ['dark', 'grim', 'death', 'tragic'],
            'lighthearted': ['funny', 'happy', 'joy', 'comedy'],
            'serious': ['serious', 'dramatic', 'emotional'],
            'suspenseful': ['suspense', 'mystery', 'thriller'],
            'inspirational': ['inspire', 'hope', 'triumph']
        };

        for (const [tone, indicators] of Object.entries(toneIndicators)) {
            if (indicators.some(indicator => title.includes(indicator))) {
                return tone;
            }
        }

        return 'neutral';
    }

    determineAudience(genres) {
        if (genres.includes('horror') || genres.includes('thriller')) {
            return 'adult';
        } else if (genres.includes('comedy') || genres.includes('animation')) {
            return 'family';
        } else if (genres.includes('romance')) {
            return 'teen-adult';
        } else {
            return 'general';
        }
    }

    processUserQuery(query) {
        // Convert natural language query to search criteria
        const searchCriteria = {
            original_query: query,
            preferred_genres: this.extractGenresFromQuery(query),
            excluded_genres: this.extractExclusions(query),
            preferred_themes: this.extractThemesFromQuery(query),
            preferred_tone: this.analyzeQueryTone(query)
        };

        // Generate search vector based on criteria
        searchCriteria.search_vector = this.generateSearchVector(searchCriteria);
        
        return searchCriteria;
    }

    extractGenresFromQuery(query) {
        const genres = [];
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('comedy') || queryLower.includes('funny')) {
            genres.push('comedy');
        }
        if (queryLower.includes('drama') || queryLower.includes('serious')) {
            genres.push('drama');
        }
        if (queryLower.includes('action') || queryLower.includes('adventure')) {
            genres.push('action');
        }
        if (queryLower.includes('thriller') || queryLower.includes('suspense')) {
            genres.push('thriller');
        }
        if (queryLower.includes('romance') || queryLower.includes('love')) {
            genres.push('romance');
        }
        if (queryLower.includes('horror') || queryLower.includes('scary')) {
            genres.push('horror');
        }

        return genres.length > 0 ? genres : ['drama', 'thriller'];
    }

    extractExclusions(query) {
        const exclusions = [];
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('no comedy') || queryLower.includes('not funny')) {
            exclusions.push('comedy');
        }
        if (queryLower.includes('no horror') || queryLower.includes('not scary')) {
            exclusions.push('horror');
        }
        if (queryLower.includes('no romance')) {
            exclusions.push('romance');
        }

        return exclusions;
    }

    extractThemesFromQuery(query) {
        const themes = [];
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('psychological') || queryLower.includes('mind')) {
            themes.push('psychological');
        }
        if (queryLower.includes('family') || queryLower.includes('parent')) {
            themes.push('family');
        }
        if (queryLower.includes('friendship') || queryLower.includes('friend')) {
            themes.push('friendship');
        }
        if (queryLower.includes('revenge')) {
            themes.push('revenge');
        }

        return themes;
    }

    analyzeQueryTone(query) {
        const queryLower = query.toLowerCase();
        
        if (queryLower.includes('dark') || queryLower.includes('grim')) {
            return 'dark';
        } else if (queryLower.includes('light') || queryLower.includes('fun')) {
            return 'lighthearted';
        } else if (queryLower.includes('suspenseful') || queryLower.includes('tense')) {
            return 'suspenseful';
        } else {
            return 'neutral';
        }
    }

    generateSearchVector(searchCriteria) {
        // Create a simple search vector based on criteria
        // In a real implementation, this would use sentence embeddings
        const vector = new Array(50).fill(0);
        
        // Boost dimensions based on preferred genres
        searchCriteria.preferred_genres.forEach(genre => {
            const hash = this.stringToHash(genre) % 50;
            vector[hash] += 0.3;
        });
        
        // Penalize excluded genres
        searchCriteria.excluded_genres.forEach(genre => {
            const hash = this.stringToHash(genre) % 50;
            vector[hash] -= 0.5;
        });

        return vector;
    }

    stringToHash(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            hash = ((hash << 5) - hash) + str.charCodeAt(i);
            hash |= 0;
        }
        return Math.abs(hash);
    }

    cosineSimilarity(vecA, vecB) {
        const dotProduct = vecA.reduce((sum, a, i) => sum + a * vecB[i], 0);
        const normA = Math.sqrt(vecA.reduce((sum, a) => sum + a * a, 0));
        const normB = Math.sqrt(vecB.reduce((sum, b) => sum + b * b, 0));
        return dotProduct / (normA * normB);
    }

    async getEnhancedRecommendations(userQuery, topK = 10) {
        await this.initialize();
        
        // Process user query
        const searchCriteria = this.processUserQuery(userQuery);
        
        // Get recommendations
        const recommendations = [];
        
        for (let i = 0; i < this.itemEmbeddings.length; i++) {
            const movie = this.movieData[i];
            const llmFeatures = this.llmFeatures[movie.id];
            
            // Calculate similarity
            const similarity = this.cosineSimilarity(
                searchCriteria.search_vector, 
                this.itemEmbeddings[i]
            );
            
            // Apply genre filters
            let finalScore = similarity;
            if (searchCriteria.excluded_genres.some(genre => 
                llmFeatures.genres.includes(genre))) {
                finalScore *= 0.1; // Heavy penalty for excluded genres
            }
            
            // Generate explanation
            const explanation = this.generateExplanation(movie.title, searchCriteria, llmFeatures);
            
            recommendations.push({
                id: movie.id,
                title: movie.title,
                score: finalScore,
                llm_genres: llmFeatures.genres,
                llm_themes: llmFeatures.themes,
                llm_tone: llmFeatures.tone,
                explanation: explanation,
                year: movie.year || ''
            });
        }
        
        // Sort by score and return top K
        return recommendations
            .sort((a, b) => b.score - a.score)
            .slice(0, topK);
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
        if (llmFeatures.themes.some(theme => 
            searchCriteria.preferred_themes.includes(theme))) {
            reasons.push('thematic depth');
        }
        
        // Check tone matches
        if (llmFeatures.tone === searchCriteria.preferred_tone && 
            searchCriteria.preferred_tone !== 'neutral') {
            reasons.push(`${llmFeatures.tone} atmosphere`);
        }
        
        if (reasons.length > 0) {
            return `Recommended because it matches your interest in ${reasons.join(' and ')}`;
        } else {
            return 'Recommended based on high-quality content matching general preferences';
        }
    }

    // Keep traditional method for backward compatibility
    async getTraditionalRecommendations(userId, topK = 10) {
        await this.initialize();
        
        const userVector = this.userEmbeddings[userId];
        const recommendations = [];
        
        for (let i = 0; i < this.itemEmbeddings.length; i++) {
            const similarity = this.cosineSimilarity(userVector, this.itemEmbeddings[i]);
            recommendations.push({
                id: this.movieData[i].id,
                title: this.movieData[i].title,
                score: similarity,
                year: this.movieData[i].year || ''
            });
        }
        
        return recommendations
            .sort((a, b) => b.score - a.score)
            .slice(0, topK);
    }
}

// Initialize global instance
window.EnhancedTwoTower = new EnhancedTwoTower();
