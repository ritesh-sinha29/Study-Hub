import Link from "next/link";
import { buttonVariants } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { ArrowRight, Sparkles } from "lucide-react";

export function Hero() {
  return (
    <section className="relative flex flex-1 flex-col items-center justify-center px-4 py-24 sm:px-6 lg:px-8">
      {/* Background gradient */}
      <div className="absolute inset-0 -z-10">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent" />
      </div>

      <div className="mx-auto flex max-w-4xl flex-col items-center text-center">
        {/* Badge */}
        <Badge variant="secondary" className="mb-6 gap-1.5 px-3 py-1 text-xs">
          <Sparkles className="size-3" />
          <span>Now in Public Beta</span>
        </Badge>

        {/* Headline */}
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
          Learn Faster.
          <br />
          <span className="bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            Build Smarter.
          </span>
        </h1>

        {/* Subtitle */}
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-muted-foreground sm:text-lg">
          An interactive learning platform designed for developers.
          Master new skills with hands-on projects, AI-powered guidance,
          and a community that helps you grow.
        </p>

        {/* CTA Button */}
        <div className="mt-8 flex flex-col items-center">
          <Link
            href="/dashboard"
            className={cn(
              buttonVariants({ size: "lg" }),
              "h-11 gap-2 px-6 text-base inline-flex items-center"
            )}
          >
            Start Learning <ArrowRight className="size-4 ml-1" />
          </Link>
        </div>

        {/* Social proof */}
        <p className="mt-8 text-xs text-muted-foreground">
          Trusted by <span className="font-medium text-foreground">500+</span>{" "}
          developers across{" "}
          <span className="font-medium text-foreground">30+</span> countries
        </p>
      </div>
    </section>
  );
}
