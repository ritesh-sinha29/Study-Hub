import { createClient } from "@convex-dev/better-auth";
import { convex } from "@convex-dev/better-auth/plugins";
import { type GenericCtx, isRunMutationCtx } from "@convex-dev/better-auth/utils";
import type { BetterAuthOptions } from "better-auth";
import { betterAuth } from "better-auth";

import { components, internal } from "../_generated/api";
import type { DataModel } from "../_generated/dataModel";
import authConfig from "../auth.config";
import schema from "./schema";

// Better Auth Component
export const authComponent = createClient<DataModel, typeof schema>(
  components.betterAuth as any,
  {
    local: { schema },
    verbose: false,
  },
);

// Better Auth Options
export const createAuthOptions = (ctx: GenericCtx<DataModel>) => {
  const providers: BetterAuthOptions["socialProviders"] = {};

  if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
    providers.google = {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    };
  }

  const baseURL =
    process.env.SITE_URL ||
    process.env.BETTER_AUTH_URL ||
    "http://localhost:3000";

  // Dynamically build trusted origins from SITE_URL
  const trustedOrigins = Array.from(
    new Set([baseURL, "http://localhost:3000"].filter(Boolean)),
  );

  return {
    appName: "Study-Hub",
    baseURL: baseURL,
    trustedOrigins: trustedOrigins,
    secret: process.env.BETTER_AUTH_SECRET,
    database: authComponent.adapter(ctx),
    socialProviders: providers,
    account: {
      accountLinking: {
        enabled: true,
      },
    },

    plugins: [
      convex({ authConfig }) as any,
    ],

    // Sync better-auth users to the main Convex user table
    databaseHooks: {
      user: {
        create: {
          after: async (user) => {
            try {
              if (isRunMutationCtx(ctx)) {
                await ctx.runMutation(internal.users.syncUserCreated, {
                  id: user.id,
                  name: user.name || "",
                  email: user.email,
                  emailVerified: user.emailVerified || false,
                  image: user.image || null,
                });
              }
            } catch (err) {
              console.error("Failed to sync created user:", err);
            }
          },
        },
        update: {
          after: async (user) => {
            try {
              if (isRunMutationCtx(ctx)) {
                await ctx.runMutation(internal.users.syncUserUpdated, {
                  id: user.id,
                  name: user.name || "",
                  email: user.email,
                  emailVerified: user.emailVerified || false,
                  image: user.image || null,
                });
              }
            } catch (err) {
              console.error("Failed to sync updated user:", err);
            }
          },
        },
      },
    },
  } satisfies BetterAuthOptions;
};

// For `auth` CLI
export const options = createAuthOptions({} as GenericCtx<DataModel>);

// Better Auth Instance
export const createAuth = (ctx: GenericCtx<DataModel>) => {
  return betterAuth(createAuthOptions(ctx));
};
