export interface Post {
  id: string;
  title: string;
  author: string;
  tool_category: string;
  media_url: string;
  media_type: 'image' | 'video';
  stats: {
    likes: number;
    reposts: number;
  };
  extracted_prompt: string;
  extracted_negative?: string;
  fetch_date: string;
}
