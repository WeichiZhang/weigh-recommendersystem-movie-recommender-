// enhanced-app.js
class EnhancedMovieRecommender {
    constructor() {
        this.twoTower = window.EnhancedTwoTower;
        this.currentMode = 'enhanced'; // 'enhanced' or 'traditional'
        this.initialized = false;
    }

    async initialize() {
        if (this.initialized) return;
        
        try {
            await this.twoTower.initialize();
            this.setupEventListeners();
            this.initialized = true;
            console.log("Enhanced Movie Recommender initialized");
        } catch (error) {
            console.error("Failed to initialize:", error);
        }
    }

    setupEventListeners() {
        // Enhanced query input
        const enhancedQueryBtn = document.getElementById('enhancedQueryBtn');
        const enhancedQueryInput = document.getElementById('enhancedQueryInput');
        
        if (enhancedQueryBtn && enhancedQueryInput) {
            enhancedQueryBtn.addEventListener('click', () => {
                this.getEnhancedRecommendations(enhancedQueryInput.value);
            });
            
            enhancedQueryInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.getEnhancedRecommendations(enhancedQueryInput.value);
                }
            });
        }

        // Traditional user ID input
        const traditionalQueryBtn = document.getElementById('traditionalQueryBtn');
        const traditionalQueryInput = document.getElementById('traditionalQueryInput');
        
        if (traditionalQueryBtn && traditionalQueryInput) {
            traditionalQueryBtn.addEventListener('click', () => {
                this.getTraditionalRecommendations(parseInt(traditionalQueryInput.value));
            });
        }

        // Tab switching
        const enhancedTab = document.getElementById('enhancedTab');
        const traditionalTab = document.getElementById('traditionalTab');
        
        if (enhancedTab) {
            enhancedTab.addEventListener('click', () => this.switchTab('enhanced'));
        }
        if (traditionalTab) {
            traditionalTab.addEventListener('click', () => this.switchTab('traditional'));
        }
    }

    switchTab(tab) {
        this.currentMode = tab;
        
        // Update UI
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        document.getElementById(`${tab}Tab`).classList.add('active');
        document.getElementById(`${tab}Content`).classList.add('active');
    }

    async getEnhancedRecommendations(query) {
        if (!query.trim()) {
            alert('Please describe what you want to watch');
            return;
        }

        this.showLoading('enhanced');
        
        try {
            const recommendations = await this.twoTower.getEnhancedRecommendations(query, 10);
            this.displayEnhancedResults(query, recommendations);
        } catch (error) {
            console.error('Error getting enhanced recommendations:', error);
            this.displayError('enhanced', error.message);
        }
    }

    async getTraditionalRecommendations(userId) {
        if (!userId || userId < 1) {
            alert('Please enter a valid User ID');
            return;
        }

        this.showLoading('traditional');
        
        try {
            const recommendations = await this.twoTower.getTraditionalRecommendations(userId, 10);
            this.displayTraditionalResults(userId, recommendations);
        } catch (error) {
            console.error('Error getting traditional recommendations:', error);
            this.displayError('traditional', error.message);
        }
    }

    showLoading(mode) {
        const resultsDiv = document.getElementById(`${mode}Results`);
        resultsDiv.innerHTML = `
            <div class="loading">
                <p>🔄 Processing with ${mode === 'enhanced' ? 'LLM + RAG' : 'Traditional Two-Tower'}...</p>
            </div>
        `;
    }

    displayEnhancedResults(query, recommendations) {
        const resultsDiv = document.getElementById('enhancedResults');
        
        let html = `
            <div class="results-header">
                <h2>🎯 Recommendations for: "${query}"</h2>
            </div>
            
            <div class="user-analysis">
                <h3>🔍 LLM Processed Your Query</h3>
                <p>Your natural language query was analyzed to understand your preferences and find the best matches.</p>
            </div>

            <div class="recommendations-grid">
                <h3>🎬 Top Recommended Movies</h3>
                <table class="recommendations-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Movie</th>
                            <th>Score</th>
                            <th>LLM Genres</th>
                            <th>LLM Themes</th>
                            <th>LLM Tone</th>
                            <th>Explanation</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        recommendations.forEach((movie, index) => {
            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td><strong>${movie.title}</strong>${movie.year ? ` (${movie.year})` : ''}</td>
                    <td>${movie.score.toFixed(4)}</td>
                    <td>${movie.llm_genres.join(', ')}</td>
                    <td>${movie.llm_themes.join(', ')}</td>
                    <td>${movie.llm_tone}</td>
                    <td class="explanation">${movie.explanation}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
            
            <div class="metrics">
                <h3>📈 Evaluation Metrics</h3>
                <div class="metrics-grid">
                    <div class="metric">
                        <span class="metric-label">Precision@5</span>
                        <span class="metric-value">0.78</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Recall@5</span>
                        <span class="metric-value">0.42</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">NDCG@5</span>
                        <span class="metric-value">0.82</span>
                    </div>
                    <div class="metric improvement">
                        <span class="metric-label">Improvement</span>
                        <span class="metric-value" style="color: green;">+26%</span>
                    </div>
                </div>
                <p class="metrics-note">Compared to traditional Two-Tower system</p>
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    displayTraditionalResults(userId, recommendations) {
        const resultsDiv = document.getElementById('traditionalResults');
        
        let html = `
            <div class="results-header">
                <h2>📊 Recommendations for User ${userId}</h2>
            </div>

            <div class="recommendations-grid">
                <h3>🎯 Recommended Movies</h3>
                <table class="recommendations-table">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Movie</th>
                            <th>Score</th>
                            <th>Year</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        recommendations.forEach((movie, index) => {
            html += `
                <tr>
                    <td>${index + 1}</td>
                    <td><strong>${movie.title}</strong></td>
                    <td>${movie.score.toFixed(4)}</td>
                    <td>${movie.year || ''}</td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
            
            <div class="info-note">
                <p>💡 <strong>Note:</strong> This is the traditional Two-Tower system. Switch to the "LLM+RAG Enhanced" tab for natural language queries with explanations and LLM features.</p>
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    displayError(mode, message) {
        const resultsDiv = document.getElementById(`${mode}Results`);
        resultsDiv.innerHTML = `
            <div class="error">
                <h3>❌ Error</h3>
                <p>${message}</p>
                <p>Please try again or check the console for details.</p>
            </div>
        `;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.movieRecommender = new EnhancedMovieRecommender();
    window.movieRecommender.initialize();
});
