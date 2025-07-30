setupQualityChecks() {
    this.qualityCheckers = {
        'python': this.checkPythonQuality.bind(this),
        'javascript': this.checkJavaScriptQuality.bind(this),
        'typescript': this.checkTypeScriptQuality.bind(this),
        'java': this.checkJavaQuality.bind(this),
        'cpp': this.checkCppQuality.bind(this),
    };
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
            <button onclick="this.viewFile('${result.id}')">View</button>
            <button onclick="this.analyzeFile('${result.id}')">Analyze</button>
        </div>
    `;
    
    // Add to chat
    const chatContainer = document.querySelector('.chat-container') || document.querySelector('.messages');
    if (chatContainer) {
        chatContainer.appendChild(fileContainer);
    }
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
`;

// Add styles to document
const styleSheet = document.createElement('style');
styleSheet.textContent = styles;
document.head.appendChild(styleSheet);