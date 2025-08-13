// Code copy functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons to all code blocks
    document.querySelectorAll('.highlight').forEach(function(codeBlock, index) {
        // Create copy button
        const button = document.createElement('button');
        button.className = 'copy-code-button';
        button.textContent = 'Copy';
        button.setAttribute('data-clipboard-target', '#code-block-' + index);
        
        // Add ID to code block
        codeBlock.id = 'code-block-' + index;
        
        // Add button to code block
        codeBlock.style.position = 'relative';
        codeBlock.appendChild(button);
        
        // Add click event
        button.addEventListener('click', function() {
            const code = codeBlock.querySelector('code');
            const text = code.innerText || code.textContent;
            
            // Copy to clipboard
            navigator.clipboard.writeText(text).then(function() {
                // Success feedback
                button.textContent = 'Copied!';
                button.classList.add('copy-success');
                
                setTimeout(function() {
                    button.textContent = 'Copy';
                    button.classList.remove('copy-success');
                }, 2000);
            }).catch(function(err) {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                
                try {
                    document.execCommand('copy');
                    button.textContent = 'Copied!';
                    button.classList.add('copy-success');
                    
                    setTimeout(function() {
                        button.textContent = 'Copy';
                        button.classList.remove('copy-success');
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy: ', err);
                    button.textContent = 'Failed';
                    setTimeout(function() {
                        button.textContent = 'Copy';
                    }, 2000);
                }
                
                document.body.removeChild(textArea);
            });
        });
    });
    
    // Enhanced code block styling
    document.querySelectorAll('pre code').forEach(function(block) {
        // Add language label if data-lang is present
        const language = block.getAttribute('data-lang') || 
                        block.className.replace('language-', '') || 
                        'text';
        
        if (language && language !== 'text') {
            const parent = block.closest('.highlight');
            if (parent && !parent.querySelector('.code-lang')) {
                const langLabel = document.createElement('div');
                langLabel.className = 'code-lang';
                langLabel.textContent = language.toUpperCase();
                langLabel.style.cssText = `
                    position: absolute;
                    top: 8px;
                    left: 12px;
                    font-size: 11px;
                    color: #656d76;
                    font-weight: 500;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    z-index: 1;
                `;
                parent.appendChild(langLabel);
            }
        }
        
        // Line numbers (optional)
        const lines = block.textContent.split('\n').length;
        if (lines > 5) {
            const lineNumbers = document.createElement('div');
            lineNumbers.className = 'line-numbers';
            lineNumbers.style.cssText = `
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 40px;
                background: #f6f8fa;
                border-right: 1px solid #d0d7de;
                padding: 16px 8px;
                font-family: var(--font-mono);
                font-size: 12px;
                line-height: 1.5;
                color: #656d76;
                text-align: right;
                user-select: none;
            `;
            
            let lineNumbersHTML = '';
            for (let i = 1; i <= lines; i++) {
                lineNumbersHTML += i + '\n';
            }
            lineNumbers.textContent = lineNumbersHTML.trim();
            
            const parent = block.closest('.highlight');
            if (parent) {
                parent.style.paddingLeft = '50px';
                parent.appendChild(lineNumbers);
            }
        }
    });
});

// Syntax highlighting enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Add language classes for better highlighting
    document.querySelectorAll('code[class*="language-"]').forEach(function(code) {
        const language = code.className.match(/language-(\w+)/);
        if (language) {
            const parent = code.closest('pre');
            if (parent) {
                parent.setAttribute('data-lang', language[1]);
            }
        }
    });
    
    // Highlight search terms in code (if coming from search)
    const urlParams = new URLSearchParams(window.location.search);
    const searchTerm = urlParams.get('highlight');
    
    if (searchTerm) {
        document.querySelectorAll('code').forEach(function(code) {
            const text = code.innerHTML;
            const regex = new RegExp(`(${searchTerm})`, 'gi');
            code.innerHTML = text.replace(regex, '<mark>$1</mark>');
        });
    }
});