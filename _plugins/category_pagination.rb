module Jekyll
  class CategoryPageGenerator < Generator
    safe true
    priority :lowest

    def generate(site)
      return unless site.config['category_pagination_enabled']
      
      posts_per_page = site.config['category_posts_per_page'] || 5
      
      # Get all categories
      categories = site.posts.docs.flat_map { |post| post.data['categories'] || [] }.uniq
      
      categories.each do |category|
        category_posts = site.posts.docs.select { |post| 
          (post.data['categories'] || []).include?(category) 
        }.sort_by(&:date).reverse
        
        total_pages = (category_posts.size.to_f / posts_per_page).ceil
        
        (1..total_pages).each do |page_num|
          site.pages << CategoryPage.new(site, category, page_num, posts_per_page, total_pages)
        end
      end
    end
  end

  class CategoryPage < Page
    def initialize(site, category, page_num, posts_per_page, total_pages)
      @site = site
      @base = site.source
      @dir = page_num == 1 ? "category/#{category}" : "category/#{category}/page/#{page_num}"
      @name = 'index.html'

      self.process(@name)
      self.read_yaml(File.join(@base, '_layouts'), 'category.html')
      
      self.data['category'] = category
      self.data['title'] = "#{category} 카테고리"
      self.data['page'] = page_num
      self.data['total_pages'] = total_pages
      
      # Calculate posts for this page
      all_posts = site.posts.docs.select { |post| 
        (post.data['categories'] || []).include?(category) 
      }.sort_by(&:date).reverse
      
      offset = (page_num - 1) * posts_per_page
      self.data['posts'] = all_posts[offset, posts_per_page] || []
    end
  end
end