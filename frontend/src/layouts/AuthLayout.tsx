interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
}

export default function AuthLayout({ children, title }: AuthLayoutProps) {
  return (
    <div className="flex justify-center min-h-screen my-8">
      <div className="w-96 px-4 py-4">
        <div>
          <h2 className="mt-6 text-center text-2xl font-bold text-gray-900 dark:text-gray-100">
            {title}
          </h2>
          {children}
        </div>
      </div>
    </div>
  );
}
