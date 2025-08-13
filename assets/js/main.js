document.addEventListener('DOMContentLoaded', function() {
    // Table of Contents Generator
    function generateTOC() {
        const tocNav = document.getElementById('toc-nav');
        if (!tocNav) return;

        const postBody = document.querySelector('.post-body');
        if (!postBody) return;

        // Find all headings in the post body
        const headings = postBody.querySelectorAll('h1, h2, h3, h4, h5, h6');
        
        if (headings.length === 0) {
            tocNav.innerHTML = '<p style="color: #94a3b8; font-size: 13px;">목차가 없습니다</p>';
            return;
        }

        // Generate TOC HTML
        const tocList = document.createElement('ul');
        
        headings.forEach((heading, index) => {
            // Create unique ID for heading if it doesn't exist
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }

            const level = heading.tagName.toLowerCase();
            const text = heading.textContent.trim();
            
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            
            link.href = `#${heading.id}`;
            link.textContent = text;
            link.className = `toc-${level}`;
            link.dataset.target = heading.id;
            
            listItem.appendChild(link);
            tocList.appendChild(listItem);

            // Smooth scroll click handler
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.getElementById(heading.id);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    
                    // Update URL hash
                    history.pushState(null, null, `#${heading.id}`);
                }
            });
        });

        tocNav.appendChild(tocList);
    }

    // Scroll Progress and Active Section Tracking
    function updateScrollProgress() {
        const progressBar = document.querySelector('.toc-progress-bar');
        const scrollPercentage = document.querySelector('.scroll-percentage');
        const tocLinks = document.querySelectorAll('.toc-nav a');
        
        if (!progressBar || !scrollPercentage) return;

        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        // Update progress bar
        if (progressBar) {
            progressBar.style.setProperty('--progress', `${Math.min(scrollPercent, 100)}%`);
        }
        if (scrollPercentage) {
            scrollPercentage.textContent = `${Math.round(scrollPercent)}%`;
        }

        // Update active section
        const headings = document.querySelectorAll('.post-body h1, .post-body h2, .post-body h3, .post-body h4, .post-body h5, .post-body h6');
        let activeHeading = null;

        // Find the current active heading
        for (let i = headings.length - 1; i >= 0; i--) {
            const heading = headings[i];
            const rect = heading.getBoundingClientRect();
            
            if (rect.top <= 100) { // 100px offset from top
                activeHeading = heading;
                break;
            }
        }

        // Update active state in TOC
        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (activeHeading && link.dataset.target === activeHeading.id) {
                link.classList.add('active');
            }
        });
    }

    // Intersection Observer for better performance
    function setupIntersectionObserver() {
        const headings = document.querySelectorAll('.post-body h1, .post-body h2, .post-body h3, .post-body h4, .post-body h5, .post-body h6');
        const tocLinks = document.querySelectorAll('.toc-nav a');
        
        if (headings.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const id = entry.target.id;
                const link = document.querySelector(`.toc-nav a[data-target="${id}"]`);
                
                if (entry.isIntersecting) {
                    // Remove active class from all links
                    tocLinks.forEach(l => l.classList.remove('active'));
                    // Add active class to current link
                    if (link) {
                        link.classList.add('active');
                    }
                }
            });
        }, {
            rootMargin: '-50px 0px -50px 0px',
            threshold: 0
        });

        headings.forEach(heading => observer.observe(heading));
    }

    // Initialize everything
    generateTOC();
    
    // Set up scroll listeners
    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateScrollProgress();
                ticking = false;
            });
            ticking = true;
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    
    // Use intersection observer for modern browsers
    if ('IntersectionObserver' in window) {
        setupIntersectionObserver();
    }

    // Initial call
    updateScrollProgress();

    // Handle hash changes (back/forward navigation)
    window.addEventListener('hashchange', function() {
        const hash = window.location.hash;
        if (hash) {
            const target = document.querySelector(hash);
            if (target) {
                setTimeout(() => {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }, 100);
            }
        }
    });

    // 카테고리 필터링 기능 (기존 기능 유지)
    const categoryLinks = document.querySelectorAll('.categories a');
    
    categoryLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // 모든 카테고리 링크에서 active 클래스 제거
            categoryLinks.forEach(l => l.classList.remove('active'));
            
            // 클릭된 링크에 active 클래스 추가
            this.classList.add('active');
            
            // 실제 페이지 이동
            window.location.href = this.href;
        });
    });
});