export default function DashboardPage() {
  return (
    <div className="flex flex-1 flex-col gap-6 p-6">
      {/* Welcome Banner */}
      <div className="rounded-xl bg-gradient-to-br from-primary/10 via-primary/5 to-background border p-6 sm:p-8">
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
          Welcome back! 👋
        </h1>
        <p className="mt-2 text-muted-foreground max-w-lg">
          Ready to continue your learning journey? Pick up where you left off or explore something new.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-xl border bg-card p-5">
          <p className="text-sm font-medium text-muted-foreground">Courses in Progress</p>
          <p className="mt-2 text-3xl font-bold">0</p>
        </div>
        <div className="rounded-xl border bg-card p-5">
          <p className="text-sm font-medium text-muted-foreground">Completed</p>
          <p className="mt-2 text-3xl font-bold">0</p>
        </div>
        <div className="rounded-xl border bg-card p-5 sm:col-span-2 lg:col-span-1">
          <p className="text-sm font-medium text-muted-foreground">Learning Streak</p>
          <p className="mt-2 text-3xl font-bold">0 days</p>
        </div>
      </div>

      {/* Recent Activity / Empty State */}
      <div className="rounded-xl border bg-card p-8 sm:p-12 flex flex-col items-center justify-center text-center">
        <div className="flex size-12 items-center justify-center rounded-full bg-muted">
          <svg
            className="size-6 text-muted-foreground"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={1.5}
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"
            />
          </svg>
        </div>
        <h3 className="mt-4 text-lg font-semibold">No recent activity</h3>
        <p className="mt-2 text-sm text-muted-foreground max-w-xs">
          Start a course to track your learning progress and build your streak.
        </p>
      </div>
    </div>
  );
}
