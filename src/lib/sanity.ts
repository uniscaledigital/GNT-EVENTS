import { createClient } from '@sanity/client';
import imageUrlBuilder from '@sanity/image-url';

export const sanityClient = createClient({
  projectId: 'a3u7t2gg',
  dataset: 'production',
  useCdn: true, // Use CDN for faster response, disable for fresh data if needed
  apiVersion: '2024-03-01', // use a valid API version date
});

const builder = imageUrlBuilder(sanityClient);

export function urlFor(source: any) {
  return builder.image(source);
}
