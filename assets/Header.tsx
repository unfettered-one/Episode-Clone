import { Button } from "@/components/ui/button";
import { Search, Menu, User } from "lucide-react";
import { ThemeToggle } from "@/components/theme-toggle";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useEffect, useRef, useState } from "react";

const Header = () => {
  const location = useLocation();
  const isHome = location.pathname === "/";
  const isStories = location.pathname === "/stories";
  const navigate = useNavigate();
  const [searchOpen, setSearchOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [searchHover, setSearchHover] = useState(false);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const searchTimerRef = useRef<number | null>(null);

  useEffect(() => {
    // Keep the header search in sync with the URL q param when on /stories.
    // Also close and clear the search when leaving the stories page.
    const params = new URLSearchParams(location.search);
    const q = params.get("q") ?? "";

    if (isStories) {
      // If we're on /stories, reflect the q param in the local input state
      setQuery(q);
    } else {
      // Close search when leaving stories page
      setSearchOpen(false);
      setQuery("");
    }
  }, [isStories, location.search]);

  useEffect(() => {
    if (searchOpen && inputRef.current) inputRef.current.focus();
  }, [searchOpen]);

  // Auto-close search popover after 15s of inactivity if not hovered or focused
  useEffect(() => {
    const clearTimer = () => {
      if (searchTimerRef.current) {
        clearTimeout(searchTimerRef.current);
        searchTimerRef.current = null;
      }
    };

    const startTimerIfNeeded = () => {
      clearTimer();
      if (!searchOpen) return;
      // If hovered or input focused, do not start
      const focused = document.activeElement === inputRef.current;
      if (searchHover || focused) return;
      searchTimerRef.current = window.setTimeout(() => {
        setSearchOpen(false);
      }, 50);
    };

    startTimerIfNeeded();

    return () => clearTimer();
  }, [searchOpen, searchHover]);

  const onQueryChange = (value: string) => {
    setQuery(value);
    navigate(`/stories?q=${encodeURIComponent(value)}`);
  };

  return (
    <header className="bg-background/80 backdrop-blur-md border-b border-border/50 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
              StoryFlow
            </div>
          </div>

          {/* Navigation */}
          <nav className="hidden md:flex items-center space-x-6">
            <Link to="/" className="text-foreground hover:text-primary transition-colors duration-200">
              Discover
            </Link>
            <Link to="/coming-soon" className="text-foreground hover:text-primary transition-colors duration-200">
              Create
            </Link>
            <Link to="/coming-soon" className="text-foreground hover:text-primary transition-colors duration-200">
              Community
            </Link>
            <Link to="/stories" className="text-foreground hover:text-primary transition-colors duration-200">
              My Stories
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-3">
            {!isHome && (
              <div className="relative">
                <button
                  onClick={() => setSearchOpen(s => !s)}
                  className="p-2 rounded-md hover:bg-muted/50"
                  aria-label="Open search"
                >
                  <Search className="h-5 w-5" />
                </button>

                {isStories && searchOpen && (
                  <div
                    onMouseEnter={() => setSearchHover(true)}
                    onMouseLeave={() => setSearchHover(false)}
                    className="absolute right-0 mt-2 bg-popover p-2 rounded-md shadow-lg flex items-center space-x-2"
                  >
                    <input
                      ref={inputRef}
                      value={query}
                      onChange={e => {
                        onQueryChange(e.target.value);
                      }}
                      onFocus={() => {
                        // Cancel any pending auto-close when user focuses the input
                        if (searchTimerRef.current) {
                          clearTimeout(searchTimerRef.current);
                          searchTimerRef.current = null;
                        }
                      }}
                      onBlur={() => {
                        // Close immediately when input loses focus unless the popover is hovered.
                        // Use setTimeout(0) to allow click events (e.g., Clear) to fire first.
                        setTimeout(() => {
                          if (!searchHover) setSearchOpen(false);
                        }, 0);
                      }}
                      placeholder="Search stories..."
                      className="bg-transparent outline-none text-foreground px-2 w-64"
                    />
                    <button onClick={() => { setQuery(""); onQueryChange(""); }} className="text-muted-foreground">Clear</button>
                  </div>
                )}
              </div>
            )}
            
            <ThemeToggle />
            
            <Link to="/coming-soon">
              <Button variant="outline" className="hidden sm:flex">
                <User className="h-4 w-4 mr-2" />
                Profile
              </Button>
            </Link>

            <Link to="/coming-soon">
              <Button className="bg-gradient-to-r from-primary to-secondary hover:opacity-90 transition-opacity">
                Create Story
              </Button>
            </Link>

            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;