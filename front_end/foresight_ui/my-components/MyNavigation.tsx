"use client";

import * as React from 'react';
import { NavigationMenu } from '@base-ui/react/navigation-menu';
import Link from 'next/link';
import Image from 'next/image';
import { 
  Home, 
  Trophy, 
  Target, 
  BarChart3, 
  Users, 
  Calendar, 
  Globe, 
  Info, 
  UserCircle,
  LogIn,
  Menu,
  X,
  ChevronDown,
  Star,
  TrendingUp,
  Shield,
  Award,
  Circle,
  CircleDashed,
  ChevronRight,
  Newspaper,
  Flame,
  Eye,
  Zap,
  MoreHorizontal
} from 'lucide-react';

export default function SportsNavigationMenu() {
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);
  const [mobileSoccerOpen, setMobileSoccerOpen] = React.useState(false);
  const [mobileBasketballOpen, setMobileBasketballOpen] = React.useState(false);
  const [mobileNewsOpen, setMobileNewsOpen] = React.useState(false);
  const [isClient, setIsClient] = React.useState(false);

  // Set isClient to true when component mounts on client
  React.useEffect(() => {
    setIsClient(true);
  }, []);

  const basketballLeagues = [
    { name: 'NBA', href: '/basketball/nba' },
    { name: 'EuroLeague', href: '/basketball/euroleague' },
    { name: 'NBL', href: '/basketball/nbl' },
    { name: 'ACB', href: '/basketball/acb' },
    { name: 'CBA', href: '/basketball/cba' },
    { name: 'BBL', href: '/basketball/bbl' },
    { name: 'LNB', href: '/basketball/lnb' },
  ];

  // More compact soccer leagues for laptop screens
  const soccerTopLeagues = [
    { name: 'Champions League', href: '/soccer/champions-league', icon: <Star size={12} className="text-yellow-500" /> },
    { name: 'Premier League', href: '/soccer/premier-league', icon: <Trophy size={12} className="text-red-500" /> },
    { name: 'La Liga', href: '/soccer/la-liga', icon: <Target size={12} /> },
    { name: 'Bundesliga', href: '/soccer/bundesliga', icon: <Target size={12} /> },
    { name: 'Serie A', href: '/soccer/serie-a', icon: <Target size={12} /> },
    { name: 'Ligue 1', href: '/soccer/ligue-1', icon: <Target size={12} /> },
  ];

  const soccerOtherLeagues = [
    { name: 'Europa League', href: '/soccer/europa-league' },
    { name: 'Betway Premiership', href: '/soccer/betway-premiership' },
    { name: 'MLS', href: '/soccer/mls' },
    { name: 'Europa Conference', href: '/soccer/europa-conference' },
    { name: 'CAF Champions', href: '/soccer/caf-champions' },
    { name: 'View All Leagues', href: '/soccer/all-leagues', highlight: true },
  ];

  // Ultra-compact news categories for laptop screens
  const newsCategories = [
    {
      category: 'Sports',
      icon: <Newspaper size={12} className="text-blue-500" />,
      items: [
        { name: 'Basketball', href: '/news/basketball' },
        { name: 'Soccer', href: '/news/soccer' },
        { name: 'Breaking', href: '/news/breaking' },
      ]
    },
    {
      category: 'Analysis',
      icon: <BarChart3 size={12} className="text-green-500" />,
      items: [
        { name: 'Predictions', href: '/analysis/predictions' },
        { name: 'Player Stats', href: '/analysis/players' },
        { name: 'Team Insights', href: '/analysis/teams' },
      ]
    },
    {
      category: 'Trending',
      icon: <Flame size={12} className="text-orange-500" />,
      items: [
        { name: 'Hot Takes', href: '/trending/takes' },
        { name: 'Transfers', href: '/trending/transfers' },
        { name: 'Viral', href: '/trending/viral' },
      ]
    },
    {
      category: 'More',
      icon: <MoreHorizontal size={12} className="text-purple-500" />,
      items: [
        { name: 'Previews', href: '/features/previews' },
        { name: 'All News', href: '/news/all', highlight: true },
        { name: 'Insights', href: '/insights' },
      ]
    }
  ];

  // Don't render until client-side to avoid hydration mismatch
  if (!isClient) {
    return (
      <nav className="w-full bg-background-layer-1 border-b border-foreground/10 shadow-raised fixed top-0 left-0 right-0 z-50">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="relative w-10 h-10 bg-foreground/10 rounded-lg animate-pulse" />
              <div className="w-24 h-6 bg-foreground/10 rounded animate-pulse" />
            </div>
            <div className="hidden lg:flex items-center space-x-2">
              <div className="w-16 h-9 bg-foreground/10 rounded-full animate-pulse" />
              <div className="w-24 h-9 bg-foreground/10 rounded-full animate-pulse" />
              <div className="w-24 h-9 bg-foreground/10 rounded-full animate-pulse" />
              <div className="w-20 h-9 bg-foreground/10 rounded-full animate-pulse" />
              <div className="w-32 h-9 bg-foreground/10 rounded-full animate-pulse" />
            </div>
            <div className="w-9 h-9 bg-foreground/10 rounded-lg animate-pulse lg:hidden" />
          </div>
        </div>
      </nav>
    );
  }

  return (
    <>
      {/* Fixed navigation bar at the very top */}
      <nav 
        className="w-full bg-background-layer-1 border-b border-foreground/10 shadow-raised fixed top-0 left-0 right-0 z-50"
        suppressHydrationWarning
      >
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <Link href="/" className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
                <div className="relative w-10 h-10">
                  <Image
                    src="/logo.png"
                    alt="Sports Predictions Logo"
                    fill
                    className="object-contain"
                    priority
                  />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                  SportStat
                </span>
              </Link>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center space-x-1">
              <NavigationMenu.Root>
                <NavigationMenu.List className="flex items-center space-x-1">
                  
                  {/* Home */}
                  <NavigationMenu.Item>
                    <Link
                      href="/"
                      className="flex items-center space-x-2 px-4 py-2 rounded-full hover:bg-foreground/5 transition-colors text-foreground/80 hover:text-foreground"
                      suppressHydrationWarning
                    >
                      <Home size={18} />
                      <span>Home</span>
                    </Link>
                  </NavigationMenu.Item>

                  {/* Basketball Predictions - Made more compact */}
                  <NavigationMenu.Item>
                    <NavigationMenu.Trigger 
                      className="group flex items-center space-x-2 px-4 py-2 rounded-full hover:bg-foreground/5 transition-colors text-foreground/80 hover:text-foreground data-[state=open]:bg-foreground/5 data-[state=open]:text-foreground"
                      suppressHydrationWarning
                    >
                      <Circle size={18} />
                      <span>Basketball</span>
                      <ChevronDown className="w-4 h-4 transition-transform group-data-[state=open]:rotate-180" />
                    </NavigationMenu.Trigger>
                    <NavigationMenu.Content className="absolute top-full left-0 w-[500px] bg-background-layer-1 border border-foreground/10 rounded-lg shadow-raised mt-2 p-3 overflow-hidden">
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-primary">
                            <Trophy size={14} />
                            Leagues
                          </h3>
                          <ul className="space-y-1">
                            {basketballLeagues.map((league) => (
                              <li key={league.name}>
                                <Link href={league.href} className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                  <Target size={12} />
                                  <span className="text-sm">{league.name}</span>
                                </Link>
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-primary">
                            <BarChart3 size={14} />
                            Analysis
                          </h3>
                          <ul className="space-y-1">
                            <li>
                              <Link href="/basketball/predictions" className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                <TrendingUp size={12} />
                                <span className="text-sm">Predictions</span>
                              </Link>
                            </li>
                            <li>
                              <Link href="/basketball/player-stats" className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                <Users size={12} />
                                <span className="text-sm">Player Stats</span>
                              </Link>
                            </li>
                            <li>
                              <Link href="/basketball/team-analysis" className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                <BarChart3 size={12} />
                                <span className="text-sm">Team Analysis</span>
                              </Link>
                            </li>
                            <li>
                              <Link href="/basketball/schedule" className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                <Calendar size={12} />
                                <span className="text-sm">Schedule</span>
                              </Link>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </NavigationMenu.Content>
                  </NavigationMenu.Item>

                  {/* Soccer Predictions - Ultra compact for laptop screens */}
                  <NavigationMenu.Item>
                    <NavigationMenu.Trigger 
                      className="group flex items-center space-x-2 px-4 py-2 rounded-full hover:bg-foreground/5 transition-colors text-foreground/80 hover:text-foreground data-[state=open]:bg-foreground/5 data-[state=open]:text-foreground"
                      suppressHydrationWarning
                    >
                      <CircleDashed size={18} />
                      <span>Soccer</span>
                      <ChevronDown className="w-4 h-4 transition-transform group-data-[state=open]:rotate-180" />
                    </NavigationMenu.Trigger>
                    <NavigationMenu.Content className="absolute top-full left-0 w-[600px] bg-background-layer-1 border border-foreground/10 rounded-lg shadow-raised mt-2 p-3 overflow-hidden">
                      <div className="grid grid-cols-2 gap-4">
                        {/* Top Soccer Leagues */}
                        <div>
                          <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-primary">
                            <Trophy size={14} />
                            Top Leagues
                          </h3>
                          <ul className="space-y-1">
                            {soccerTopLeagues.map((league) => (
                              <li key={league.name}>
                                <Link href={league.href} className="flex items-center gap-2 p-1.5 rounded hover:bg-foreground/5 transition-colors">
                                  {league.icon}
                                  <span className="text-sm">{league.name}</span>
                                </Link>
                              </li>
                            ))}
                          </ul>
                        </div>

                        {/* Other Leagues & Quick Links */}
                        <div className="space-y-4">
                          <div>
                            <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-primary">
                              <Globe size={14} />
                              More Leagues
                            </h3>
                            <ul className="grid grid-cols-2 gap-1">
                              {soccerOtherLeagues.map((league) => (
                                <li key={league.name}>
                                  <Link 
                                    href={league.href} 
                                    className={`flex items-center gap-1.5 p-1.5 rounded hover:bg-foreground/5 transition-colors ${league.highlight ? 'text-primary font-medium' : ''}`}
                                  >
                                    <Target size={10} />
                                    <span className="text-xs">{league.name}</span>
                                  </Link>
                                </li>
                              ))}
                            </ul>
                          </div>
                          
                          {/* Quick Soccer Links */}
                          <div>
                            <h3 className="font-semibold text-sm mb-2 flex items-center gap-2 text-primary">
                              <BarChart3 size={14} />
                              Quick Links
                            </h3>
                            <div className="flex gap-2">
                              <Link href="/soccer/predictions" className="flex-1 text-center text-xs p-1.5 rounded bg-primary/5 hover:bg-primary/10 text-primary transition-colors">
                                Predictions
                              </Link>
                              <Link href="/soccer/standings" className="flex-1 text-center text-xs p-1.5 rounded bg-primary/5 hover:bg-primary/10 text-primary transition-colors">
                                Standings
                              </Link>
                              <Link href="/soccer/news" className="flex-1 text-center text-xs p-1.5 rounded bg-primary/5 hover:bg-primary/10 text-primary transition-colors">
                                News
                              </Link>
                            </div>
                          </div>
                        </div>
                      </div>
                    </NavigationMenu.Content>
                  </NavigationMenu.Item>

                  {/* News - Ultra compact for laptop screens */}
                  <NavigationMenu.Item>
                    <NavigationMenu.Trigger 
                      className="group flex items-center space-x-2 px-4 py-2 rounded-full hover:bg-foreground/5 transition-colors text-foreground/80 hover:text-foreground data-[state=open]:bg-foreground/5 data-[state=open]:text-foreground"
                      suppressHydrationWarning
                    >
                      <Newspaper size={18} />
                      <span>News</span>
                      <ChevronDown className="w-4 h-4 transition-transform group-data-[state=open]:rotate-180" />
                    </NavigationMenu.Trigger>
                    <NavigationMenu.Content className="absolute top-full left-0 w-[500px] bg-background-layer-1 border border-foreground/10 rounded-lg shadow-raised mt-2 p-3 overflow-hidden">
                      <div className="grid grid-cols-4 gap-2">
                        {newsCategories.map((category) => (
                          <div key={category.category} className="space-y-1">
                            <h3 className="font-semibold text-xs mb-1 flex items-center gap-1 text-foreground/70">
                              {category.icon}
                              <span>{category.category}</span>
                            </h3>
                            <ul className="space-y-0.5">
                              {category.items.map((item) => (
                                <li key={item.name}>
                                  <Link 
                                    href={item.href} 
                                    className={`block p-1.5 rounded hover:bg-foreground/5 transition-colors text-xs ${item.highlight ? 'bg-primary/5 text-primary font-medium' : 'text-foreground'}`}
                                  >
                                    {item.name}
                                  </Link>
                                </li>
                              ))}
                            </ul>
                          </div>
                        ))}
                      </div>
                      
                      {/* Quick News Links */}
                      <div className="mt-3 pt-3 border-t border-foreground/10">
                        <div className="flex items-center justify-between text-xs">
                          <Link 
                            href="/news/latest" 
                            className="flex items-center gap-1 text-primary hover:text-primary/80 transition-colors"
                          >
                            <Zap size={10} />
                            Latest
                          </Link>
                          <Link 
                            href="/trending" 
                            className="flex items-center gap-1 text-primary hover:text-primary/80 transition-colors"
                          >
                            <Flame size={10} />
                            Trending
                          </Link>
                          <Link 
                            href="/analysis" 
                            className="flex items-center gap-1 text-primary hover:text-primary/80 transition-colors"
                          >
                            <BarChart3 size={10} />
                            Analysis
                          </Link>
                          <Link 
                            href="/features" 
                            className="flex items-center gap-1 text-primary hover:text-primary/80 transition-colors"
                          >
                            <Eye size={10} />
                            Features
                          </Link>
                        </div>
                      </div>
                    </NavigationMenu.Content>
                  </NavigationMenu.Item>

                  {/* How It Works */}
                  <NavigationMenu.Item>
                    <Link
                      href="/how-it-works"
                      className="flex items-center space-x-2 px-4 py-2 rounded-full hover:bg-foreground/5 transition-colors text-foreground/80 hover:text-foreground"
                      suppressHydrationWarning
                    >
                      <Info size={18} />
                      <span>How It Works</span>
                    </Link>
                  </NavigationMenu.Item>

                  {/* User Auth */}
                  <div className="flex items-center space-x-2 ml-4 pl-4 border-l border-foreground/10">
                    <NavigationMenu.Item>
                      <Link
                        href="/login"
                        className="flex items-center space-x-2 px-4 py-2 rounded-full bg-gradient-to-r from-primary/10 to-secondary/10 hover:from-primary/20 hover:to-secondary/20 transition-all text-primary"
                        suppressHydrationWarning
                      >
                        <LogIn size={18} />
                        <span>Login</span>
                      </Link>
                    </NavigationMenu.Item>
                    <NavigationMenu.Item>
                      <Link
                        href="/signup"
                        className="flex items-center space-x-2 px-4 py-2 rounded-full bg-gradient-to-r from-primary to-secondary text-white hover:opacity-90 transition-opacity shadow-raised"
                        suppressHydrationWarning
                      >
                        <UserCircle size={18} />
                        <span>Sign Up</span>
                      </Link>
                    </NavigationMenu.Item>
                  </div>
                </NavigationMenu.List>

                <NavigationMenu.Portal>
                  <NavigationMenu.Positioner
                    className="absolute z-50"
                    sideOffset={5}
                    collisionPadding={20}
                  >
                    <NavigationMenu.Popup className="bg-background-layer-1 border border-foreground/10 rounded-lg shadow-raised overflow-hidden">
                      <NavigationMenu.Viewport />
                    </NavigationMenu.Popup>
                  </NavigationMenu.Positioner>
                </NavigationMenu.Portal>
              </NavigationMenu.Root>
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 rounded-lg hover:bg-foreground/5 transition-colors"
              aria-label="Toggle menu"
              suppressHydrationWarning
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </nav>

      {/* Spacer div to push content below fixed nav */}
      <div className="h-[68px] lg:h-[68px]" />

      {/* Mobile Menu - Fixed to viewport */}
      {mobileMenuOpen && (
        <div className="lg:hidden fixed top-[68px] left-0 right-0 bottom-0 bg-background-layer-1 z-40 overflow-y-auto">
          <div className="p-4 space-y-2">
            <Link
              href="/"
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-foreground/5 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
              suppressHydrationWarning
            >
              <Home size={20} />
              <span>Home</span>
            </Link>

            {/* Basketball Mobile Section */}
            <div className="space-y-1">
              <button
                onClick={() => setMobileBasketballOpen(!mobileBasketballOpen)}
                className="flex items-center justify-between w-full p-3 rounded-lg hover:bg-foreground/5 transition-colors"
                suppressHydrationWarning
              >
                <div className="flex items-center space-x-3">
                  <Circle size={20} />
                  <span className="font-medium">Basketball</span>
                </div>
                <ChevronRight className={`w-4 h-4 transition-transform ${mobileBasketballOpen ? 'rotate-90' : ''}`} />
              </button>
              {mobileBasketballOpen && (
                <div className="ml-6 space-y-1 pl-2 border-l border-foreground/10">
                  <div className="font-medium text-sm text-foreground/70 mb-2 mt-2">Leagues</div>
                  {basketballLeagues.map((league) => (
                    <Link 
                      key={league.name}
                      href={league.href} 
                      className="flex items-center space-x-2 p-2 rounded hover:bg-foreground/5 transition-colors"
                      onClick={() => setMobileMenuOpen(false)}
                      suppressHydrationWarning
                    >
                      <Target size={14} />
                      <span className="text-sm">{league.name}</span>
                    </Link>
                  ))}
                  <div className="font-medium text-sm text-foreground/70 mb-2 mt-3">Analysis</div>
                  <Link href="/basketball/predictions" className="flex items-center space-x-2 p-2 rounded hover:bg-foreground/5">
                    <TrendingUp size={14} />
                    <span className="text-sm">Predictions</span>
                  </Link>
                  <Link href="/basketball/player-stats" className="flex items-center space-x-2 p-2 rounded hover:bg-foreground/5">
                    <Users size={14} />
                    <span className="text-sm">Player Stats</span>
                  </Link>
                </div>
              )}
            </div>

            {/* Soccer Mobile Section */}
            <div className="space-y-1">
              <button
                onClick={() => setMobileSoccerOpen(!mobileSoccerOpen)}
                className="flex items-center justify-between w-full p-3 rounded-lg hover:bg-foreground/5 transition-colors"
                suppressHydrationWarning
              >
                <div className="flex items-center space-x-3">
                  <CircleDashed size={20} />
                  <span className="font-medium">Soccer</span>
                </div>
                <ChevronRight className={`w-4 h-4 transition-transform ${mobileSoccerOpen ? 'rotate-90' : ''}`} />
              </button>
              {mobileSoccerOpen && (
                <div className="ml-6 space-y-1 pl-2 border-l border-foreground/10 max-h-[50vh] overflow-y-auto">
                  <div className="font-medium text-sm text-foreground/70 mb-2 mt-2">Top Leagues</div>
                  {soccerTopLeagues.map((league) => (
                    <Link 
                      key={league.name}
                      href={league.href} 
                      className="flex items-center space-x-2 p-2 rounded hover:bg-foreground/5 transition-colors"
                      onClick={() => setMobileMenuOpen(false)}
                      suppressHydrationWarning
                    >
                      {league.icon}
                      <span className="text-sm">{league.name}</span>
                    </Link>
                  ))}
                  
                  <div className="font-medium text-sm text-foreground/70 mb-2 mt-3">More Leagues</div>
                  <div className="grid grid-cols-2 gap-2">
                    {soccerOtherLeagues.map((league) => (
                      <Link 
                        key={league.name}
                        href={league.href} 
                        className={`flex items-center space-x-2 p-2 rounded hover:bg-foreground/5 transition-colors ${league.highlight ? 'text-primary font-medium' : ''}`}
                        onClick={() => setMobileMenuOpen(false)}
                        suppressHydrationWarning
                      >
                        <Target size={12} />
                        <span className="text-xs">{league.name}</span>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* News Mobile Section */}
            <div className="space-y-1">
              <button
                onClick={() => setMobileNewsOpen(!mobileNewsOpen)}
                className="flex items-center justify-between w-full p-3 rounded-lg hover:bg-foreground/5 transition-colors"
                suppressHydrationWarning
              >
                <div className="flex items-center space-x-3">
                  <Newspaper size={20} />
                  <span className="font-medium">News</span>
                </div>
                <ChevronRight className={`w-4 h-4 transition-transform ${mobileNewsOpen ? 'rotate-90' : ''}`} />
              </button>
              {mobileNewsOpen && (
                <div className="ml-6 space-y-1 pl-2 border-l border-foreground/10">
                  {newsCategories.map((category) => (
                    <div key={category.category} className="mb-3">
                      <div className="font-medium text-xs text-foreground/70 mb-1.5 mt-2 flex items-center gap-2">
                        {category.icon}
                        {category.category}
                      </div>
                      {category.items.map((item) => (
                        <Link 
                          key={item.name}
                          href={item.href} 
                          className={`block p-1.5 rounded hover:bg-foreground/5 transition-colors text-sm ${item.highlight ? 'bg-primary/5 text-primary font-medium' : ''}`}
                          onClick={() => setMobileMenuOpen(false)}
                          suppressHydrationWarning
                        >
                          {item.name}
                        </Link>
                      ))}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <Link
              href="/how-it-works"
              className="flex items-center space-x-3 p-3 rounded-lg hover:bg-foreground/5 transition-colors"
              onClick={() => setMobileMenuOpen(false)}
              suppressHydrationWarning
            >
              <Info size={20} />
              <span>How It Works</span>
            </Link>

            <div className="pt-4 space-y-2">
              <Link
                href="/login"
                className="flex items-center justify-center space-x-2 p-3 rounded-lg bg-gradient-to-r from-primary/10 to-secondary/10 text-primary font-medium"
                onClick={() => setMobileMenuOpen(false)}
                suppressHydrationWarning
              >
                <LogIn size={20} />
                <span>Login</span>
              </Link>
              <Link
                href="/signup"
                className="flex items-center justify-center space-x-2 p-3 rounded-lg bg-gradient-to-r from-primary to-secondary text-white font-medium shadow-raised"
                onClick={() => setMobileMenuOpen(false)}
                suppressHydrationWarning
              >
                <UserCircle size={20} />
                <span>Sign Up</span>
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  );
}