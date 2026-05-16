"use client";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, Autoplay } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

export function Carousel({ slides, perView = 1, autoplay = false }: { slides: React.ReactNode[]; perView?: number; autoplay?: boolean }) {
  return (
    <Swiper
      modules={[Navigation, Pagination, Autoplay]}
      navigation
      pagination={{ type: "fraction" }}
      autoplay={autoplay ? { delay: 4000 } : false}
      slidesPerView={1}
      breakpoints={{ 768: { slidesPerView: perView } }}
      speed={600}
    >
      {slides.map((s, i) => <SwiperSlide key={i}>{s}</SwiperSlide>)}
    </Swiper>
  );
}
