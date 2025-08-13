module Jekyll
  module ReadingTimeFilter
    # Calculate reading time based on word count
    # Assuming average reading speed of 200 words per minute
    def reading_time(input)
      words_per_minute = 200
      
      # Strip HTML tags and count words
      words = input.to_s.gsub(/<[^>]*>/, '').split.size
      
      # Calculate reading time in minutes
      time = (words.to_f / words_per_minute).ceil
      
      # Return appropriate text based on time
      case time
      when 0, 1
        "1분 읽기"
      else
        "#{time}분 읽기"
      end
    end
    
    # Get word count
    def word_count(input)
      input.to_s.gsub(/<[^>]*>/, '').split.size
    end
  end
end

Liquid::Template.register_filter(Jekyll::ReadingTimeFilter)