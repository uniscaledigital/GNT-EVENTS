import { createFileRoute } from "@tanstack/react-router";
import { SiteLayout, PageHeader } from "@/components/site/Layout";
import { sanityClient, urlFor } from "@/lib/sanity";

type GalleryImage = {
  _id: string;
  title: string;
  imageUrl: string;
  alt: string;
};
export const Route = createFileRoute("/gallery")({
  head: () => ({
    meta: [
      { title: "Gallery — GNT Events & Decorators" },
      { name: "description", content: "A curated album of weddings, receptions and celebrations designed by GNT Events & Decorators." },
    ],
  }),
  loader: async () => {
    const images: GalleryImage[] = await sanityClient.fetch(
      `*[_type == "galleryImage"]{ _id, title, "imageUrl": image.asset->url, alt }`
    );
    return { images };
  },
  component: Gallery,
});

function Gallery() {
  const { images } = Route.useLoaderData();

  return (
    <SiteLayout>
      <PageHeader
        eyebrow="The Album"
        title="Celebrations We've Crafted"
        subtitle="A small selection from our recent weddings, receptions and private events."
      />
      <section className="px-6 lg:px-10 max-w-7xl mx-auto pb-28">
        <div className="columns-1 md:columns-2 lg:columns-3 gap-6 [column-fill:_balance]">
          {images && images.map((img) => (
            <figure key={img._id} className="mb-6 break-inside-avoid group">
              <div className="rounded-3xl overflow-hidden">
                <img src={img.imageUrl} alt={img.alt || img.title} loading="lazy" className="w-full h-auto object-cover group-hover:scale-105 transition-transform duration-[1.2s]" />
              </div>
            </figure>
          ))}
        </div>
      </section>
    </SiteLayout>
  );
}
