/**
 * Enhanced Chat Interface for OpenHands Premium
 * Provides quality mode toggle, smart suggestions, and code execution features
 */
class EnhancedChatInterface {
    constructor() {
        this.setupQualityToggle();
        this.setupSmartSuggestions();
        this.setupCodeActions();
        this.setupKeyboardShortcuts();
        this.setupAutoSave();
        console.log('Enhanced Chat Interface initialized');
    }

    setupQualityToggle() {
        // Create quality toggle UI
        const toggleContainer = document.createElement('div');
        toggleContainer.className = 'quality-toggle';
        toggleContainer.innerHTML = `
            <label class="toggle-switch">
                <input type="checkbox" id="quality-mode-toggle">
                <span class="slider">Quality Mode</span>
            </label>
        `;
        document.body.appendChild(toggleContainer);

        // Add event listener
        const toggle = document.getElementById('quality-mode-toggle');
        toggle.addEventListener('change', this.toggleQualityMode.bind(this));

        // Initialize from localStorage
        const qualityMode = localStorage.getItem('qualityMode') === 'true';
        toggle.checked = qualityMode;
        this.setQualityMode(qualityMode);
    }

    toggleQualityMode(event) {
        const enabled = event.target.checked;
        this.setQualityMode(enabled);
        localStorage.setItem('qualityMode', enabled);
    }

    setQualityMode(enabled) {
        document.body.classList.toggle('quality-mode', enabled);
        
        // Update model selection if available
        const modelSelector = document.querySelector('.model-selector select');
        if (modelSelector) {
            if (enabled) {
                // Set to Claude Sonnet or GPT-4o for quality mode
                const preferredModels = ['anthropic/claude-3-5-sonnet-20241022', 'gpt-4o'];
                for (const model of preferredModels) {
                    const option = Array.from(modelSelector.options).find(opt => opt.value === model);
                    if (option) {
                        modelSelector.value = model;
                        break;
                    }
                }
            } else {
                // Set to faster model for standard mode
                modelSelector.value = 'gpt-4o-mini';
            }
        }

        // Show notification
        this.showNotification(`Quality Mode ${enabled ? 'Enabled' : 'Disabled'}`, 'info');
    }

    setupSmartSuggestions() {
        const inputArea = document.querySelector('.chat-input textarea') || 
                         document.querySelector('.chat-input input');
        
        if (!inputArea) return;
        
        // Create suggestions container
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'smart-suggestions';
        suggestionsContainer.style.display = 'none';
        inputArea.parentNode.appendChild(suggestionsContainer);
        
        // Add input event listener
        inputArea.addEventListener('input', this.handleInput.bind(this));
    }

    handleInput(event) {
        const input = event.target.value;
        const lastWord = input.split(' ').pop();
        
        if (lastWord.length < 3) {
            this.hideSuggestions();
            return;
        }
        
        // Generate suggestions based on context
        const suggestions = this.generateSuggestions(input, lastWord);
        
        if (suggestions.length > 0) {
            this.showSuggestions(suggestions);
        } else {
            this.hideSuggestions();
        }
    }

    generateSuggestions(input, lastWord) {
        // Simple suggestion generation based on common programming tasks
        const suggestions = [];
        
        const commonCommands = [
            'Create a new file',
            'Run tests',
            'Debug the code',
            'Optimize performance',
            'Add documentation',
            'Refactor the code',
            'Fix security issues',
            'Implement feature',
            'Analyze code quality'
        ];
        
        for (const command of commonCommands) {
            if (command.toLowerCase().includes(lastWord.toLowerCase())) {
                suggestions.push(command);
            }
        }
        
        return suggestions.slice(0, 5); // Limit to 5 suggestions
    }

    showSuggestions(suggestions) {
        const container = document.querySelector('.smart-suggestions');
        if (!container) return;
        
        container.innerHTML = '';
        container.style.display = 'block';
        
        for (const suggestion of suggestions) {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.textContent = suggestion;
            item.addEventListener('click', () => this.applySuggestion(suggestion));
            container.appendChild(item);
        }
    }

    hideSuggestions() {
        const container = document.querySelector('.smart-suggestions');
        if (container) {
            container.style.display = 'none';
        }
    }

    applySuggestion(suggestion) {
        const inputArea = document.querySelector('.chat-input textarea') || 
                         document.querySelector('.chat-input input');
        
        if (!inputArea) return;
        
        const currentText = inputArea.value;
        const lastSpaceIndex = currentText.lastIndexOf(' ');
        
        if (lastSpaceIndex === -1) {
            inputArea.value = suggestion;
        } else {
            inputArea.value = currentText.substring(0, lastSpaceIndex + 1) + suggestion;
        }
        
        this.hideSuggestions();
        inputArea.focus();
    }

    setupCodeActions() {
        // Add code action buttons to code blocks
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.addedNodes.length) {
                    const codeBlocks = document.querySelectorAll('pre code');
                    codeBlocks.forEach(this.addCodeActions.bind(this));
                }
            });
        });
        
        observer.observe(document.body, { childList: true, subtree: true });
    }

    addCodeActions(codeBlock) {
        // Skip if already processed
        if (codeBlock.dataset.processed) return;
        codeBlock.dataset.processed = 'true';
        
        const container = codeBlock.parentNode;
        const actionsContainer = document.createElement('div');
        actionsContainer.className = 'code-actions';
        
        // Copy button
        const copyButton = document.createElement('button');
        copyButton.textContent = 'Copy';
        copyButton.addEventListener('click', () => this.copyCode(codeBlock));
        
        // Run button
        const runButton = document.createElement('button');
        runButton.textContent = 'Run';
        runButton.addEventListener('click', () => this.runCode(codeBlock));
        
        // Quality check button
        const qualityButton = document.createElement('button');
        qualityButton.textContent = 'Quality';
        qualityButton.addEventListener('click', () => this.checkCodeQuality(codeBlock));
        
        actionsContainer.appendChild(copyButton);
        actionsContainer.appendChild(runButton);
        actionsContainer.appendChild(qualityButton);
        
        container.style.position = 'relative';
        container.appendChild(actionsContainer);
    }

    copyCode(codeBlock) {
        const code = codeBlock.textContent;
        navigator.clipboard.writeText(code)
            .then(() => this.showNotification('Code copied to clipboard', 'success'))
            .catch(() => this.showNotification('Failed to copy code', 'error'));
    }

    runCode(codeBlock) {
        const code = codeBlock.textContent;
        const language = codeBlock.className.replace('language-', '');
        
        // Create result container
        const resultContainer = document.createElement('div');
        resultContainer.className = 'execution-result';
        resultContainer.innerHTML = '<h4>Execution Result</h4><div class="result-content">Running...</div>';
        
        codeBlock.parentNode.after(resultContainer);
        
        // Simulate execution (in a real implementation, this would send to a backend)
        setTimeout(() => {
            resultContainer.querySelector('.result-content').textContent = 'Code execution is not implemented in this demo.';
        }, 1000);
    }

    checkCodeQuality(codeBlock) {
        const code = codeBlock.textContent;
        const language = codeBlock.className.replace('language-', '');
        
        // Create quality container
        const qualityContainer = document.createElement('div');
        qualityContainer.className = 'quality-analysis';
        qualityContainer.innerHTML = '<h4>Quality Analysis</h4><div class="analysis-content">Analyzing...</div>';
        
        codeBlock.parentNode.after(qualityContainer);
        
        // Simulate quality check
        setTimeout(() => {
            const issues = [];
            const suggestions = [];
            
            // Basic checks
            if (code.includes('console.log')) {
                issues.push('Remove console.log statements in production code');
            }
            
            if (code.length > 200 && !code.includes('function')) {
                suggestions.push('Consider breaking code into functions');
            }
            
            // Display results
            qualityContainer.innerHTML = `
                <h4>Quality Analysis</h4>
                <div class="quality-score">Score: ${Math.max(0, 100 - issues.length * 10)}/100</div>
                ${issues.length > 0 ? `
                    <div class="issues">
                        <h5>Issues:</h5>
                        <ul>${issues.map(issue => `<li>${issue}</li>`).join('')}</ul>
                    </div>
                ` : ''}
                ${suggestions.length > 0 ? `
                    <div class="suggestions">
                        <h5>Suggestions:</h5>
                        <ul>${suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}</ul>
                    </div>
                ` : ''}
            `;
        }, 1000);
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Ctrl+Enter to send message
            if (event.ctrlKey && event.key === 'Enter') {
                const sendButton = document.querySelector('.chat-input button');
                if (sendButton) {
                    sendButton.click();
                }
            }
            
            // Ctrl+/ to toggle quality mode
            if (event.ctrlKey && event.key === '/') {
                const toggle = document.getElementById('quality-mode-toggle');
                if (toggle) {
                    toggle.checked = !toggle.checked;
                    toggle.dispatchEvent(new Event('change'));
                }
            }
        });
    }

    setupAutoSave() {
        // Auto-save conversation every 30 seconds
        setInterval(() => {
            this.saveConversation();
        }, 30000);
        
        // Save on page unload
        window.addEventListener('beforeunload', () => {
            this.saveConversation();
        });
    }

    saveConversation() {
        const messages = document.querySelectorAll('.message');
        if (messages.length === 0) return;
        
        const conversation = Array.from(messages).map(msg => {
            const isUser = msg.classList.contains('user-message');
            const content = msg.querySelector('.message-content').textContent;
            return { role: isUser ? 'user' : 'assistant', content };
        });
        
        localStorage.setItem('savedConversation', JSON.stringify(conversation));
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

/**
 * Enhanced File Upload for OpenHands Premium
 * Provides drag-and-drop file upload with quality analysis
 */
class EnhancedFileUpload {
    constructor() {
        this.maxFileSize = 100 * 1024 * 1024; // 100MB
        this.allowedTypes = ['code', 'text', 'document', 'image'];
        this.setupDropZone();
        this.setupFileInput();
        this.setupQualityChecks();
        console.log('Enhanced File Upload initialized');
    }
    
    setupQualityChecks() {
        this.qualityCheckers = {
            'python': this.checkPythonQuality.bind(this),
            'javascript': this.checkJavaScriptQuality.bind(this),
            'typescript': this.checkTypeScriptQuality.bind(this),
            'java': this.checkJavaQuality.bind(this),
            'cpp': this.checkCppQuality.bind(this),
        };
    }
    
    setupDropZone() {
        // Create drop zone UI
        const dropZone = document.createElement('div');
        dropZone.className = 'drop-zone';
        dropZone.innerHTML = `
            <div class="drop-icon">📁</div>
            <div class="drop-text">Drag & Drop Files</div>
            <div class="drop-hint">or click to browse</div>
        `;
        
        // Add event listeners
        dropZone.addEventListener('dragover', this.handleDragOver.bind(this));
        dropZone.addEventListener('dragleave', this.handleDragLeave.bind(this));
        dropZone.addEventListener('drop', this.handleDrop.bind(this));
        dropZone.addEventListener('click', this.openFileDialog.bind(this));
        
        // Add to chat interface
        const chatContainer = document.querySelector('.chat-container') || 
                             document.querySelector('.messages');
        if (chatContainer) {
            chatContainer.appendChild(dropZone);
        } else {
            // If chat container not found, add to body
            document.body.appendChild(dropZone);
        }
    }
    
    setupFileInput() {
        // Create hidden file input
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.multiple = true;
        this.fileInput.style.display = 'none';
        this.fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        
        document.body.appendChild(this.fileInput);
    }
    
    handleDragLeave(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('drag-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('drag-over');
        
        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }

    openFileDialog() {
        this.fileInput.click();
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
    }

    async processFiles(files) {
        for (const file of files) {
            if (this.validateFile(file)) {
                await this.uploadFile(file);
            }
        }
    }

    validateFile(file) {
        // Check file size
        if (file.size > this.maxFileSize) {
            this.showError(`File ${file.name} is too large (max ${this.maxFileSize / 1024 / 1024}MB)`);
            return false;
        }

        // Check file type
        const fileType = this.getFileType(file);
        if (!this.allowedTypes.includes(fileType)) {
            this.showError(`File type not supported: ${file.name}`);
            return false;
        }

        return true;
    }

    getFileType(file) {
        const extension = file.name.split('.').pop().toLowerCase();
        
        const typeMap = {
            'py': 'code',
            'js': 'code',
            'ts': 'code',
            'java': 'code',
            'cpp': 'code',
            'c': 'code',
            'h': 'code',
            'css': 'code',
            'html': 'code',
            'txt': 'text',
            'md': 'text',
            'pdf': 'document',
            'doc': 'document',
            'docx': 'document',
            'png': 'image',
            'jpg': 'image',
            'jpeg': 'image',
            'gif': 'image',
        };

        return typeMap[extension] || 'unknown';
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                await this.handleUploadSuccess(file, result);
            } else {
                this.showError(`Upload failed: ${result.error}`);
            }
        } catch (error) {
            this.showError(`Upload failed: ${error.message}`);
        }
    }

    async handleUploadSuccess(file, result) {
        this.showSuccess(`File uploaded: ${file.name}`);
        
        // If it's a code file, run quality checks
        if (this.getFileType(file) === 'code') {
            await this.runQualityCheck(file, result.content);
        }
        
        // Add file to chat context
        this.addFileToChat(file, result);
    }

    async runQualityCheck(file, content) {
        const extension = file.name.split('.').pop().toLowerCase();
        const checker = this.qualityCheckers[extension];
        
        if (checker) {
            const qualityResult = await checker(content);
            this.displayQualityResult(file.name, qualityResult);
        }
    }

    async checkPythonQuality(content) {
        // Basic Python quality checks
        const issues = [];
        const suggestions = [];
        
        // Check for common issues
        if (content.includes('import *')) {
            issues.push('Avoid wildcard imports');
        }
        
        if (!content.includes('def ') && content.length > 100) {
            suggestions.push('Consider organizing code into functions');
        }
        
        // Check for docstrings
        const functionCount = (content.match(/def \w+/g) || []).length;
        const docstringCount = (content.match(/"""/g) || []).length / 2;
        
        if (functionCount > docstringCount) {
            suggestions.push('Add docstrings to functions');
        }
        
        return {
            score: Math.max(0, 100 - issues.length * 10),
            issues,
            suggestions
        };
    }

    async checkJavaScriptQuality(content) {
        const issues = [];
        const suggestions = [];
        
        // Check for var usage
        if (content.includes('var ')) {
            issues.push('Use const or let instead of var');
        }
        
        // Check for console.log
        if (content.includes('console.log')) {
            suggestions.push('Remove console.log statements in production');
        }
        
        // Check for == usage
        if (content.includes('==') && !content.includes('===')) {
            issues.push('Use === instead of ==');
        }
        
        return {
            score: Math.max(0, 100 - issues.length * 10),
            issues,
            suggestions
        };
    }

    async checkTypeScriptQuality(content) {
        const jsResult = await this.checkJavaScriptQuality(content);
        
        // Additional TypeScript checks
        if (!content.includes(': ') && content.includes('function')) {
            jsResult.suggestions.push('Add type annotations');
        }
        
        return jsResult;
    }

    async checkJavaQuality(content) {
        const issues = [];
        const suggestions = [];
        
        // Check for public class
        if (!content.includes('public class')) {
            suggestions.push('Consider using proper class structure');
        }
        
        // Check for main method
        if (content.includes('public static void main')) {
            suggestions.push('Consider separating main logic into methods');
        }
        
        return {
            score: Math.max(0, 100 - issues.length * 10),
            issues,
            suggestions
        };
    }

    async checkCppQuality(content) {
        const issues = [];
        const suggestions = [];
        
        // Check for includes
        if (!content.includes('#include')) {
            issues.push('Missing include statements');
        }
        
        // Check for namespace
        if (content.includes('using namespace std')) {
            suggestions.push('Avoid using namespace std in headers');
        }
        
        return {
            score: Math.max(0, 100 - issues.length * 10),
            issues,
            suggestions
        };
    }

    displayQualityResult(filename, result) {
        const qualityContainer = document.createElement('div');
        qualityContainer.className = 'file-quality-result';
        qualityContainer.innerHTML = `
            <h4>Quality Analysis: ${filename}</h4>
            <div class="quality-score">Score: ${result.score}/100</div>
            ${result.issues.length > 0 ? `
                <div class="issues">
                    <h5>Issues:</h5>
                    <ul>${result.issues.map(issue => `<li>${issue}</li>`).join('')}</ul>
                </div>
            ` : ''}
            ${result.suggestions.length > 0 ? `
                <div class="suggestions">
                    <h5>Suggestions:</h5>
                    <ul>${result.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}</ul>
                </div>
            ` : ''}
        `;
        
        // Add to chat
        const chatContainer = document.querySelector('.chat-container') || document.querySelector('.messages');
        if (chatContainer) {
            chatContainer.appendChild(qualityContainer);
        }
    }

    addFileToChat(file, result) {
        const fileContainer = document.createElement('div');
        fileContainer.className = 'uploaded-file';
        fileContainer.innerHTML = `
            <div class="file-info">
                <span class="file-icon">📄</span>
                <span class="file-name">${file.name}</span>
                <span class="file-size">(${this.formatFileSize(file.size)})</span>
            </div>
            <div class="file-actions">
                <button class="view-file-btn" data-file-id="${result.id}">View</button>
                <button class="analyze-file-btn" data-file-id="${result.id}">Analyze</button>
            </div>
        `;
        
        // Add event listeners
        const viewBtn = fileContainer.querySelector('.view-file-btn');
        const analyzeBtn = fileContainer.querySelector('.analyze-file-btn');
        
        viewBtn.addEventListener('click', () => this.viewFile(result.id));
        analyzeBtn.addEventListener('click', () => this.analyzeFile(result.id));
        
        // Add to chat
        const chatContainer = document.querySelector('.chat-container') || document.querySelector('.messages');
        if (chatContainer) {
            chatContainer.appendChild(fileContainer);
        }
    }
    
    viewFile(fileId) {
        // In a real implementation, this would fetch the file content from the server
        this.showNotification('Viewing file...', 'info');
        
        // Simulate file viewing
        setTimeout(() => {
            const fileViewer = document.createElement('div');
            fileViewer.className = 'file-viewer';
            fileViewer.innerHTML = `
                <div class="file-viewer-header">
                    <h3>File Viewer</h3>
                    <button class="close-viewer-btn">×</button>
                </div>
                <div class="file-viewer-content">
                    <p>File content would be displayed here.</p>
                    <p>File ID: ${fileId}</p>
                </div>
            `;
            
            // Add close button event listener
            const closeBtn = fileViewer.querySelector('.close-viewer-btn');
            closeBtn.addEventListener('click', () => fileViewer.remove());
            
            document.body.appendChild(fileViewer);
        }, 500);
    }
    
    analyzeFile(fileId) {
        // In a real implementation, this would analyze the file on the server
        this.showNotification('Analyzing file...', 'info');
        
        // Simulate file analysis
        setTimeout(() => {
            const analysisResult = document.createElement('div');
            analysisResult.className = 'file-analysis-result';
            analysisResult.innerHTML = `
                <h4>File Analysis</h4>
                <div class="analysis-content">
                    <p>File ID: ${fileId}</p>
                    <div class="analysis-metrics">
                        <div class="metric">
                            <span class="metric-name">Quality Score:</span>
                            <span class="metric-value">85/100</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">Security Score:</span>
                            <span class="metric-value">90/100</span>
                        </div>
                        <div class="metric">
                            <span class="metric-name">Performance Score:</span>
                            <span class="metric-value">80/100</span>
                        </div>
                    </div>
                    <div class="analysis-recommendations">
                        <h5>Recommendations:</h5>
                        <ul>
                            <li>Add more comprehensive error handling</li>
                            <li>Improve documentation coverage</li>
                            <li>Consider optimizing performance-critical sections</li>
                        </ul>
                    </div>
                </div>
            `;
            
            // Add to chat
            const chatContainer = document.querySelector('.chat-container') || document.querySelector('.messages');
            if (chatContainer) {
                chatContainer.appendChild(analysisResult);
            }
        }, 1500);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Initialize enhancements when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new EnhancedChatInterface();
    new EnhancedFileUpload();
});

// Add CSS styles
const styles = `
.quality-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1000;
}

.toggle-switch {
    position: relative;
    display: inline-block;
    width: 120px;
    height: 34px;
}

.toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 34px;
    padding-left: 40px;
    line-height: 34px;
    font-size: 12px;
    color: white;
}

.slider:before {
    position: absolute;
    content: "";
    height: 26px;
    width: 26px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: #2196F3;
}

input:checked + .slider:before {
    transform: translateX(26px);
}

.code-actions {
    position: absolute;
    top: 10px;
    right: 10px;
    display: flex;
    gap: 5px;
}

.code-actions button {
    padding: 5px 10px;
    border: none;
    border-radius: 4px;
    background: #007acc;
    color: white;
    cursor: pointer;
    font-size: 12px;
}

.code-actions button:hover {
    background: #005a9e;
}

.smart-suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    z-index: 1000;
}

.suggestion-item {
    padding: 10px;
    cursor: pointer;
    border-bottom: 1px solid #eee;
}

.suggestion-item:hover {
    background: #f5f5f5;
}

.suggestion-item:last-child {
    border-bottom: none;
}

.execution-result, .quality-analysis, .file-quality-result {
    margin: 10px 0;
    padding: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #f9f9f9;
}

.quality-score {
    font-weight: bold;
    color: #007acc;
    margin-bottom: 10px;
}

.issues h5, .suggestions h5 {
    color: #d73a49;
    margin: 10px 0 5px 0;
}

.suggestions h5 {
    color: #28a745;
}

.drop-zone {
    border: 2px dashed #ddd;
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    margin: 20px 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.drop-zone:hover, .drop-zone.drag-over {
    border-color: #007acc;
    background: #f0f8ff;
}

.drop-icon {
    font-size: 48px;
    margin-bottom: 10px;
}

.drop-text {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 5px;
}

.drop-hint {
    font-size: 14px;
    color: #666;
}

.uploaded-file {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin: 10px 0;
    background: white;
}

.file-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.file-actions {
    display: flex;
    gap: 5px;
}

.file-actions button {
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    cursor: pointer;
}

.file-actions button:hover {
    background: #f5f5f5;
}

.notification {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 20px;
    border-radius: 4px;
    color: white;
    font-weight: bold;
    z-index: 10000;
    animation: slideDown 0.3s ease;
}

.notification-success {
    background: #28a745;
}

.notification-error {
    background: #dc3545;
}

.notification-info {
    background: #17a2b8;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateX(-50%) translateY(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
}

.file-viewer {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    max-width: 800px;
    max-height: 80vh;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    z-index: 10000;
    display: flex;
    flex-direction: column;
    animation: fadeIn 0.3s ease;
}

.file-viewer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid #eee;
}

.file-viewer-header h3 {
    margin: 0;
    font-size: 18px;
}

.close-viewer-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.file-viewer-content {
    padding: 20px;
    overflow-y: auto;
    max-height: calc(80vh - 60px);
}

.file-analysis-result {
    margin: 15px 0;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background: #f9f9f9;
}

.analysis-metrics {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin: 15px 0;
}

.metric {
    background: white;
    padding: 10px 15px;
    border-radius: 4px;
    border: 1px solid #eee;
    display: flex;
    flex-direction: column;
}

.metric-name {
    font-size: 14px;
    color: #666;
}

.metric-value {
    font-size: 18px;
    font-weight: bold;
    color: #007acc;
}

.analysis-recommendations h5 {
    color: #28a745;
    margin: 15px 0 10px 0;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translate(-50%, -55%);
    }
    to {
        opacity: 1;
        transform: translate(-50%, -50%);
    }
}
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);