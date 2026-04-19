# Example Workflows - AI Coding Agent System

**Version:** 1.0  
**Date:** April 19, 2026  
**Purpose:** Real-world usage scenarios demonstrating system capabilities

---

## Overview

This document provides detailed, step-by-step examples of common workflows using the Einstein AI Coding Agent System. Each workflow shows the user interaction, system behavior, and expected output.

---

## Workflow Categories

1. **Simple Scripts** - Quick code generation
2. **Full-Stack Apps** - Complete application building
3. **Code Editing** - AI-assisted development
4. **Browser Automation** - Task automation
5. **Hybrid Workflows** - Multi-module combinations

---

## 1. Simple Scripts

### Workflow 1.1: Web Scraper

**User Goal:** Create a Python script to scrape HackerNews top stories

#### Voice Command
```
User: "Hey Einstein, write a Python script to scrape HackerNews top stories"
```

#### System Flow

```
[Voice Interface]
├── Wake word detected: "Hey Einstein" ✓
├── Audio capture: "write a Python script to scrape HackerNews top stories"
├── Whisper STT: Transcribing... (1.8s)
└── Transcript: "write a python script to scrape hackernews top stories"

[Einstein Orchestrator]
├── Parse intent: code_generation
├── Extract params:
│   ├── Language: Python
│   ├── Task: scrape hackernews top stories
│   └── Project: hn-scraper
├── Select model: lmstudio/qwen-coder-32b
└── Spawn sub-agent: code-generator-001

[Code Generator Sub-Agent]
├── Build prompt:
│   "You are an expert Python developer.
│    Write a script to scrape HackerNews top stories.
│    Requirements:
│    - Use requests + BeautifulSoup
│    - Print title, URL, score for top 10 stories
│    - Include error handling
│    - Add comments explaining each step"
│
├── Call LM Studio (Qwen Coder 32B)... (4.2s)
├── Code generated (89 lines)
├── Extract code from markdown
└── Validate syntax ✓

[File Manager]
├── Create project dir: ~/ai-projects/hn-scraper/
├── Save file: scraper.py
└── Make executable: chmod +x

[Code Executor] (Optional)
├── Run in OpenJarvis sandbox
├── Test with sample URL
├── Output:
│   1. Show HN: My Weekend Project (450 points)
│      https://news.ycombinator.com/item?id=12345
│   2. Ask HN: Best AI Tools 2026? (312 points)
│      ...
└── Success ✓

[Voice Response]
└── TTS: "Script ready at ~/ai-projects/hn-scraper/scraper.py
           I tested it and it works! Found 10 stories."
```

#### Generated Code

```python
#!/usr/bin/env python3
"""
HackerNews Top Stories Scraper
Fetches and displays the top stories from HackerNews front page
"""

import requests
from bs4 import BeautifulSoup
import sys

def scrape_hackernews(limit=10):
    """
    Scrape top stories from HackerNews
    
    Args:
        limit (int): Number of stories to fetch (default: 10)
    
    Returns:
        list: List of dicts with title, url, and score
    """
    try:
        # Fetch the HackerNews front page
        url = "https://news.ycombinator.com/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all story rows
        stories = []
        story_rows = soup.select('.athing')[:limit]
        
        for row in story_rows:
            # Extract title and URL
            title_elem = row.select_one('.titleline > a')
            if not title_elem:
                continue
                
            title = title_elem.get_text()
            url = title_elem.get('href', '')
            
            # Get score from next sibling row
            score_row = row.find_next_sibling('tr')
            score_elem = score_row.select_one('.score')
            score = score_elem.get_text() if score_elem else '0 points'
            
            stories.append({
                'title': title,
                'url': url,
                'score': score
            })
        
        return stories
        
    except requests.RequestException as e:
        print(f"Error fetching HackerNews: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error parsing HackerNews: {e}", file=sys.stderr)
        return []

def main():
    """Main entry point"""
    print("Fetching HackerNews top stories...\n")
    
    stories = scrape_hackernews(limit=10)
    
    if not stories:
        print("No stories found.")
        return
    
    # Print stories
    for i, story in enumerate(stories, 1):
        print(f"{i}. {story['title']} ({story['score']})")
        print(f"   {story['url']}\n")

if __name__ == "__main__":
    main()
```

#### Output Files
```
~/ai-projects/hn-scraper/
├── scraper.py           # Main script
├── requirements.txt     # Auto-generated: requests, beautifulsoup4
├── README.md            # Auto-generated usage instructions
└── .git/                # Auto-initialized
```

#### Time: ~15 seconds (voice to working script)

---

### Workflow 1.2: Data Processor

**User Goal:** Process CSV file and generate summary statistics

#### Chat Command
```
User (via OpenJarvis chat):
"Write a Python script that reads sales.csv and generates a summary report with:
- Total sales
- Average order value
- Top 5 products
- Sales by month (chart)"
```

#### System Flow

```
[Einstein]
├── Intent: code_generation
├── Input file: sales.csv (implied in user dir)
├── Output: summary script + visualizations
└── Model: qwen-coder-32b

[Code Generator]
├── Generate script with:
│   ├── pandas for CSV reading
│   ├── matplotlib for charting
│   └── argparse for CLI args
└── Time: 6.8s

[File Manager]
├── Save: ~/ai-projects/sales-analyzer/analyzer.py
├── Generate requirements.txt: pandas, matplotlib
└── Create sample sales.csv for testing
```

#### Generated Code Highlights

```python
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def analyze_sales(csv_path):
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Total sales
    total = df['amount'].sum()
    
    # Average order value
    avg = df['amount'].mean()
    
    # Top 5 products
    top_products = df.groupby('product')['amount'].sum() \
                     .sort_values(ascending=False).head(5)
    
    # Sales by month
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    monthly = df.groupby('month')['amount'].sum()
    
    # Generate chart
    monthly.plot(kind='bar')
    plt.title('Sales by Month')
    plt.savefig('sales_by_month.png')
    
    # Print summary
    print(f"Total Sales: ${total:,.2f}")
    print(f"Average Order: ${avg:,.2f}")
    print("\nTop 5 Products:")
    print(top_products)
```

---

## 2. Full-Stack Apps

### Workflow 2.1: Recipe App with Authentication

**User Goal:** Build a complete recipe sharing app

#### Voice Command
```
User: "Hey Einstein, build me a recipe app where users can create, share, and search recipes. Include user authentication."
```

#### System Flow

```
[Voice Interface] → [Einstein] → [App Builder Module]

[App Planner] (Llama 3.1 70B for complex planning)
├── Analyzing requirements... (8.5s)
├── Generated plan:
│   {
│     "name": "recipe-app",
│     "entities": [
│       { "name": "User", "fields": ["id", "email", "name", "avatar"] },
│       { "name": "Recipe", "fields": ["id", "user_id", "title", 
│                                       "ingredients", "instructions", 
│                                       "cook_time", "servings", "image"] }
│     ],
│     "features": [
│       "User signup/login",
│       "Create/edit/delete recipes",
│       "Search recipes by title/ingredient",
│       "View user profiles",
│       "Favorite recipes"
│     ],
│     "stack": {
│       "frontend": "react + vite + tailwind",
│       "backend": "supabase",
│       "auth": "supabase-auth"
│     }
│   }
└── Plan validated ✓

[Project Scaffolding]
├── Create ~/ai-projects/recipe-app/
├── Initialize Vite + React... (12s)
├── Install dependencies:
│   ├── react-router-dom
│   ├── @supabase/supabase-js
│   ├── @supabase/auth-ui-react
│   └── tailwindcss, autoprefixer, postcss
└── Setup Tailwind config ✓

[Database Generation]
├── Generate Supabase migration:
│   -- Users table (handled by Supabase Auth)
│   
│   create table recipes (
│     id uuid primary key default uuid_generate_v4(),
│     user_id uuid references auth.users not null,
│     title text not null,
│     description text,
│     ingredients jsonb not null,
│     instructions text not null,
│     cook_time integer,
│     servings integer,
│     image_url text,
│     created_at timestamp default now(),
│     updated_at timestamp default now()
│   );
│   
│   create table favorites (
│     user_id uuid references auth.users,
│     recipe_id uuid references recipes,
│     primary key (user_id, recipe_id)
│   );
│   
│   -- Enable RLS (Row Level Security)
│   alter table recipes enable row level security;
│   
│   -- Policies
│   create policy "Users can read all recipes"
│     on recipes for select using (true);
│   
│   create policy "Users can create own recipes"
│     on recipes for insert
│     with check (auth.uid() = user_id);
└── Save to: supabase/migrations/001_initial.sql

[Component Generation] (Parallel, Qwen Coder 32B)
├── Generate RecipeList.jsx... (5.2s) ✓
├── Generate RecipeCard.jsx... (4.8s) ✓
├── Generate RecipeDetail.jsx... (6.1s) ✓
├── Generate AddRecipeForm.jsx... (7.3s) ✓
├── Generate SearchBar.jsx... (3.2s) ✓
├── Generate AuthForm.jsx... (5.5s) ✓
├── Generate UserProfile.jsx... (4.9s) ✓
└── Generate Layout.jsx... (3.1s) ✓

[Routing Setup]
├── Generate App.jsx with React Router
├── Routes:
│   ├── / → Home (RecipeList)
│   ├── /recipes/:id → RecipeDetail
│   ├── /add → AddRecipeForm
│   ├── /profile → UserProfile
│   └── /login → AuthForm
└── Protected routes (require auth) ✓

[Styling]
├── Generate global styles
├── Generate Tailwind components
└── Dark mode support ✓

[Configuration]
├── Generate .env.template:
│   VITE_SUPABASE_URL=your_supabase_url
│   VITE_SUPABASE_ANON_KEY=your_anon_key
├── Generate README.md with setup instructions
└── Generate package.json scripts

[Development Server]
├── Run: npm run dev
├── Server started at: http://localhost:5173
└── Open browser automatically ✓

[Voice Response]
└── TTS: "Recipe app ready! I've created a full-stack app with user auth, 
          recipe CRUD, search, and favorites. The dev server is running 
          at localhost 5173. Check the README for Supabase setup."
```

#### Generated Project Structure

```
~/ai-projects/recipe-app/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── RecipeList.jsx          # Main recipe feed
│   │   ├── RecipeCard.jsx          # Recipe preview card
│   │   ├── RecipeDetail.jsx        # Full recipe view
│   │   ├── AddRecipeForm.jsx       # Create/edit form
│   │   ├── SearchBar.jsx           # Search interface
│   │   ├── AuthForm.jsx            # Login/signup
│   │   ├── UserProfile.jsx         # User dashboard
│   │   ├── Layout.jsx              # App shell
│   │   └── ProtectedRoute.jsx      # Auth wrapper
│   ├── lib/
│   │   └── supabase.js             # Supabase client setup
│   ├── hooks/
│   │   ├── useAuth.js              # Auth state hook
│   │   └── useRecipes.js           # Recipe data hook
│   ├── App.jsx                     # Router setup
│   ├── main.jsx                    # Entry point
│   └── index.css                   # Global styles
├── supabase/
│   └── migrations/
│       └── 001_initial.sql         # Database schema
├── .env.template                   # Environment vars
├── .gitignore
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── README.md                       # Setup instructions
└── .git/                           # Git initialized
```

#### Sample Component: RecipeCard.jsx

```jsx
import { Link } from 'react-router-dom';
import { Clock, Users, Heart } from 'lucide-react';
import { useState } from 'react';
import { supabase } from '../lib/supabase';

export default function RecipeCard({ recipe, onFavorite }) {
    const [isFavorited, setIsFavorited] = useState(recipe.isFavorited);
    const [loading, setLoading] = useState(false);

    async function handleFavorite(e) {
        e.preventDefault(); // Don't navigate when clicking heart
        setLoading(true);

        try {
            if (isFavorited) {
                await supabase
                    .from('favorites')
                    .delete()
                    .match({ recipe_id: recipe.id });
            } else {
                await supabase
                    .from('favorites')
                    .insert({ recipe_id: recipe.id });
            }
            
            setIsFavorited(!isFavorited);
            onFavorite?.(recipe.id, !isFavorited);
        } catch (error) {
            console.error('Error toggling favorite:', error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <Link to={`/recipes/${recipe.id}`}>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md 
                          overflow-hidden hover:shadow-lg transition-shadow">
                {/* Recipe image */}
                <div className="h-48 bg-gray-200 dark:bg-gray-700 
                              relative overflow-hidden">
                    {recipe.image_url ? (
                        <img
                            src={recipe.image_url}
                            alt={recipe.title}
                            className="w-full h-full object-cover"
                        />
                    ) : (
                        <div className="flex items-center justify-center h-full 
                                      text-gray-400">
                            No image
                        </div>
                    )}
                    
                    {/* Favorite button */}
                    <button
                        onClick={handleFavorite}
                        disabled={loading}
                        className="absolute top-2 right-2 p-2 rounded-full 
                                 bg-white/90 hover:bg-white transition-colors"
                    >
                        <Heart
                            className={`w-5 h-5 ${
                                isFavorited 
                                    ? 'fill-red-500 text-red-500' 
                                    : 'text-gray-600'
                            }`}
                        />
                    </button>
                </div>

                {/* Recipe info */}
                <div className="p-4">
                    <h3 className="text-xl font-semibold mb-2 text-gray-900 
                                 dark:text-white">
                        {recipe.title}
                    </h3>
                    
                    {recipe.description && (
                        <p className="text-gray-600 dark:text-gray-300 mb-3 
                                    line-clamp-2">
                            {recipe.description}
                        </p>
                    )}

                    <div className="flex items-center gap-4 text-sm 
                                  text-gray-500 dark:text-gray-400">
                        {recipe.cook_time && (
                            <div className="flex items-center gap-1">
                                <Clock className="w-4 h-4" />
                                <span>{recipe.cook_time} min</span>
                            </div>
                        )}
                        
                        {recipe.servings && (
                            <div className="flex items-center gap-1">
                                <Users className="w-4 h-4" />
                                <span>{recipe.servings} servings</span>
                            </div>
                        )}
                    </div>

                    {/* Author */}
                    <div className="mt-3 pt-3 border-t border-gray-200 
                                  dark:border-gray-700">
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                            by {recipe.author?.name || 'Anonymous'}
                        </p>
                    </div>
                </div>
            </div>
        </Link>
    );
}
```

#### README.md (Auto-generated)

```markdown
# Recipe App

A full-stack recipe sharing application built with React, Vite, Tailwind CSS, and Supabase.

## Features

- 🔐 User authentication (signup/login)
- 📝 Create, edit, and delete recipes
- 🔍 Search recipes by title or ingredients
- ❤️ Favorite recipes
- 👤 User profiles
- 🎨 Dark mode support
- 📱 Responsive design

## Setup

1. Create a Supabase project at https://supabase.com

2. Run the database migration:
   - Go to SQL Editor in Supabase dashboard
   - Run the contents of `supabase/migrations/001_initial.sql`

3. Copy `.env.template` to `.env` and fill in your Supabase credentials:
   ```bash
   cp .env.template .env
   ```

4. Install dependencies:
   ```bash
   npm install
   ```

5. Start dev server:
   ```bash
   npm run dev
   ```

6. Open http://localhost:5173

## Usage

- **Create account:** Click "Sign Up" in the navbar
- **Add recipe:** Click "+ New Recipe" (requires login)
- **Search:** Use the search bar to find recipes
- **Favorite:** Click the heart icon on any recipe card
- **Edit:** Click "Edit" on your own recipes

## Tech Stack

- **Frontend:** React 18, Vite, Tailwind CSS
- **Backend:** Supabase (PostgreSQL + Auth + Storage)
- **Routing:** React Router v6
- **Icons:** Lucide React
- **Deployment:** Vercel (recommended)

## Deploy

```bash
npm run build
vercel deploy --prod
```

Don't forget to add your Supabase environment variables in Vercel dashboard!

## Generated by Einstein AI Coding Agent
```

#### Time: ~45 seconds (voice to full working app)

---

### Workflow 2.2: Todo App (Simpler)

**User Goal:** Quick todo list app

#### Chat Command
```
User: "Build a simple todo app, no auth needed, just local storage"
```

#### System Flow

```
[App Planner]
├── Simpler requirements → faster execution
├── No backend needed (localStorage only)
├── Stack: React + Vite + Tailwind
└── Time: 3.2s

[Generation]
├── Scaffold project (8s)
├── Generate components:
│   ├── TodoList.jsx
│   ├── TodoItem.jsx
│   └── AddTodoForm.jsx
├── No database setup needed
└── Total time: 22 seconds
```

#### Key Features
- Add/delete/toggle todos
- Persist to localStorage
- Filter (all/active/completed)
- Clean UI with Tailwind
- Dark mode toggle

---

## 3. Code Editing

### Workflow 3.1: Refactor Existing Code

**User Goal:** Improve an existing component

#### Chat Command
```
User: "Refactor RecipeCard.jsx to extract the favorite button into a 
       separate component and add loading skeletons"
```

#### System Flow

```
[Code Editor Module]
├── Load file: ~/ai-projects/recipe-app/src/components/RecipeCard.jsx
├── Analyze current code (AST parsing)
├── Build context:
│   ├── Current component structure
│   ├── Dependencies (React hooks, icons)
│   └── Related components
├── Generate refactoring plan:
│   1. Extract FavoriteButton component
│   2. Create RecipeCardSkeleton component
│   3. Update RecipeCard to use new components
│   4. Add loading state
└── Model: qwen-coder-32b (6.2s)

[Code Generation]
├── Generate FavoriteButton.jsx (new file)
├── Generate RecipeCardSkeleton.jsx (new file)
├── Refactor RecipeCard.jsx (modify existing)
└── Update imports

[Git Integration]
├── Stage changes
├── Commit: "Refactor: Extract FavoriteButton, add loading skeletons"
└── Show diff for review
```

#### Generated Components

**FavoriteButton.jsx (new):**
```jsx
import { Heart } from 'lucide-react';
import { useState } from 'react';

export default function FavoriteButton({ recipeId, initialState, onToggle }) {
    const [isFavorited, setIsFavorited] = useState(initialState);
    const [loading, setLoading] = useState(false);

    async function handleClick(e) {
        e.preventDefault();
        e.stopPropagation();
        
        setLoading(true);
        try {
            const newState = !isFavorited;
            await onToggle(recipeId, newState);
            setIsFavorited(newState);
        } catch (error) {
            console.error('Failed to toggle favorite:', error);
        } finally {
            setLoading(false);
        }
    }

    return (
        <button
            onClick={handleClick}
            disabled={loading}
            className="p-2 rounded-full bg-white/90 hover:bg-white 
                     transition-colors disabled:opacity-50"
            aria-label={isFavorited ? 'Unfavorite' : 'Favorite'}
        >
            <Heart
                className={`w-5 h-5 ${
                    isFavorited 
                        ? 'fill-red-500 text-red-500' 
                        : 'text-gray-600'
                }`}
            />
        </button>
    );
}
```

**RecipeCardSkeleton.jsx (new):**
```jsx
export default function RecipeCardSkeleton() {
    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md 
                      overflow-hidden animate-pulse">
            {/* Image placeholder */}
            <div className="h-48 bg-gray-300 dark:bg-gray-700" />

            {/* Content placeholder */}
            <div className="p-4">
                {/* Title */}
                <div className="h-6 bg-gray-300 dark:bg-gray-700 rounded w-3/4 mb-2" />
                
                {/* Description */}
                <div className="space-y-2 mb-3">
                    <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded" />
                    <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-5/6" />
                </div>

                {/* Meta info */}
                <div className="flex gap-4">
                    <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-20" />
                    <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-24" />
                </div>
            </div>
        </div>
    );
}
```

#### Time: ~12 seconds (analyze + refactor + save)

---

### Workflow 3.2: Add Feature to Existing App

**User Goal:** Add export functionality to todo app

#### Voice Command
```
User: "Add a button to export todos as CSV"
```

#### System Flow

```
[Code Editor]
├── Identify target: TodoList.jsx (main component)
├── Plan changes:
│   1. Add export function
│   2. Add CSV generation logic
│   3. Add download button to UI
│   4. Style button consistently
└── Apply changes (minimal diff)

[Generated Code] (Added to TodoList.jsx)
async function exportAsCSV() {
    const csv = [
        ['Task', 'Completed', 'Created'],
        ...todos.map(todo => [
            todo.text,
            todo.completed ? 'Yes' : 'No',
            new Date(todo.createdAt).toLocaleDateString()
        ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `todos-${Date.now()}.csv`;
    a.click();
}

// In JSX:
<button onClick={exportAsCSV}
        className="px-4 py-2 bg-blue-500 text-white rounded">
    Export CSV
</button>
```

#### Time: ~8 seconds

---

## 4. Browser Automation

### Workflow 4.1: Gmail Invoice Extraction

**User Goal:** Find invoice emails and download PDFs

#### Voice Command
```
User: "Check my Gmail for invoice emails from the last month and save the PDFs to my Downloads folder"
```

#### System Flow

```
[Computer Use Module]
├── Parse task requirements:
│   ├── Platform: Gmail
│   ├── Search: "invoice" + date range (last month)
│   ├── Action: Download PDF attachments
│   └── Destination: ~/Downloads/
│
├── Generate step plan (Qwen 2.5 32B):
│   1. Navigate to gmail.com
│   2. Check if logged in (or login)
│   3. Use search box: "has:attachment invoice newer_than:1m"
│   4. For each result:
│      a. Open email
│      b. Find PDF attachments
│      c. Download to ~/Downloads/Invoices/
│   5. Report count
│
└── Execute with vision guidance...

[Execution Log]
Step 1: Navigate to Gmail
  ├── browser.goto('https://gmail.com')
  ├── Wait for load... ✓
  └── Screenshot taken

Step 2: Check login status
  ├── Screenshot analysis (LLaVA):
  │   "I see the Gmail inbox. User is logged in. Visible elements:
  │    - Search box (top center)
  │    - Compose button (top left)
  │    - Email list (center)"
  └── Status: Logged in ✓

Step 3: Perform search
  ├── Click search box
  ├── Type: "has:attachment invoice newer_than:1m"
  ├── Press Enter
  ├── Wait for results...
  └── Found 12 emails ✓

Step 4: Process emails
  [Email 1/12]
  ├── Click email
  ├── Screenshot → LLaVA:
  │   "I see an email with subject 'Invoice #1234 from Acme Corp'.
  │    There is a PDF attachment icon labeled 'invoice-1234.pdf'"
  ├── Click attachment icon
  ├── Click 'Download'
  ├── Move file: ~/Downloads/Invoices/invoice-1234.pdf
  └── Done ✓

  [Email 2/12]
  ├── Back to search results
  ├── Click email
  ├── Screenshot → LLaVA:
  │   "Email from 'Services Inc' with attachment 'receipt.pdf'"
  ├── Download attachment
  ├── Save to ~/Downloads/Invoices/receipt.pdf
  └── Done ✓

  [... 10 more emails processed ...]

Step 5: Report
  ├── Total emails: 12
  ├── PDFs downloaded: 12
  └── Location: ~/Downloads/Invoices/

[Voice Response]
└── TTS: "I found 12 invoice emails from the last month and downloaded 
          all PDF attachments to your Downloads folder in the Invoices 
          subfolder."
```

#### Safety Features

- **Confirmation before download:** "I found 12 invoices. Download all?" → User: "Yes"
- **Dry run mode:** User can preview actions without executing
- **Screenshot logging:** All steps recorded for audit

#### Time: ~3 minutes (depends on email count)

---

### Workflow 4.2: Form Filling

**User Goal:** Fill out a contact form

#### Chat Command
```
User: "Fill out the contact form at example.com/contact with:
       Name: John Doe
       Email: john@example.com
       Message: Interested in your services"
```

#### System Flow

```
[Task Executor]
├── Navigate to example.com/contact
├── Screenshot analysis:
│   "I see a contact form with 3 fields:
│    - Name (input, top)
│    - Email (input, middle)
│    - Message (textarea, bottom)
│    - Submit button (blue, bottom right)"
│
├── Execution plan:
│   1. Click name field
│   2. Type "John Doe"
│   3. Click email field
│   4. Type "john@example.com"
│   5. Click message field
│   6. Type "Interested in your services"
│   7. Click submit
│
├── Execute steps...
│   ├── Fill name ✓
│   ├── Fill email ✓
│   ├── Fill message ✓
│   └── Submit ✓
│
└── Verify:
    ├── Screenshot after submit
    ├── LLaVA: "I see a success message: 'Thank you! We'll be in touch.'"
    └── Success ✓
```

#### Time: ~15 seconds

---

### Workflow 4.3: Data Extraction

**User Goal:** Scrape product prices from e-commerce site

#### Voice Command
```
User: "Go to amazon.com, search for 'wireless mouse', and save the top 10 results with prices to a CSV"
```

#### System Flow

```
[Execution]
├── Navigate to amazon.com
├── Find search box (vision-guided)
├── Type "wireless mouse"
├── Submit search
├── Wait for results
│
├── Extract data (loop 10 times):
│   ├── Screenshot product grid
│   ├── LLaVA analysis:
│   │   "Product 1: Logitech M510 - $24.99
│   │    Product 2: Microsoft Basic - $12.99
│   │    Product 3: Razer DeathAdder - $69.99
│   │    ..."
│   └── Parse structured data
│
├── Generate CSV:
│   Rank,Product Name,Price,Rating
│   1,Logitech M510 Wireless Mouse,$24.99,4.5
│   2,Microsoft Basic Optical Mouse,$12.99,4.2
│   ...
│
└── Save to ~/Downloads/amazon-wireless-mouse-search.csv
```

#### Safety: READ-ONLY (no purchases, no account actions)

#### Time: ~45 seconds

---

## 5. Hybrid Workflows

### Workflow 5.1: Voice → App → Edit → Deploy

**Complete development cycle with AI assistance**

#### Step 1: Initial App Generation (Voice)
```
User: "Hey Einstein, build a blog platform with posts and comments"
```

**Result:** Full React + Supabase app generated in 50 seconds

---

#### Step 2: Review & Refinement (Chat)
```
User (in OpenJarvis chat):
"The blog post cards look too plain. Add a featured image, 
 author avatar, and read time estimate."
```

**System:**
```
[Code Editor]
├── Analyze BlogPostCard.jsx
├── Modify component:
│   ├── Add image prop + rendering
│   ├── Add author avatar component
│   ├── Calculate read time from post content
│   └── Update Tailwind styling
└── Time: 9s
```

**Result:** Component updated, dev server auto-refreshes

---

#### Step 3: Add Feature (Voice)
```
User: "Add rich text editing for blog posts"
```

**System:**
```
[App Builder]
├── Install dependency: @tiptap/react
├── Generate RichTextEditor.jsx component
├── Update AddPostForm.jsx to use rich text editor
├── Update database schema (content type: jsonb)
└── Time: 18s
```

---

#### Step 4: Automated Testing (Voice)
```
User: "Test the blog post creation flow"
```

**System:**
```
[Computer Use]
├── Open localhost:5173 in browser
├── Navigate to /new-post
├── Fill title: "Test Post"
├── Fill rich text editor: "This is a test"
├── Click "Publish"
├── Verify post appears in feed
└── Result: ✓ Post created successfully
```

---

#### Step 5: Deployment (Voice)
```
User: "Deploy this to production"
```

**System:**
```
[Deployment Module]
├── Run build: npm run build
├── Optimize assets
├── Deploy to Vercel:
│   ├── Create project
│   ├── Upload build
│   ├── Configure env vars (from .env)
│   └── Deploy
├── URL: https://my-blog-xyz123.vercel.app
└── Voice: "Blog deployed! Live at my-blog-xyz123.vercel.app"
```

---

#### Total Time: ~5 minutes (voice command to live production app)

---

### Workflow 5.2: Multi-Module Orchestration

**Complex task requiring multiple modules**

#### Voice Command
```
User: "Check my email for client requests, create a project for each one, 
       and reply confirming I've started work"
```

#### System Flow

```
[Einstein Orchestrator]
├── Task breakdown:
│   1. Email checking (Computer Use)
│   2. Project creation (App Builder / File Manager)
│   3. Email replies (Computer Use)
│
├── Spawn modules in sequence...
│
└── Execution:

    [Module 1: Computer Use - Email Check]
    ├── Open Gmail
    ├── Search: "label:client-requests is:unread"
    ├── Extract data:
    │   - Email 1: John Smith - "Need a landing page"
    │   - Email 2: Jane Doe - "Build a todo app"
    │   - Email 3: Acme Corp - "Create a dashboard"
    └── Pass to next module

    [Module 2: App Builder - Project Creation]
    For each request:
    ├── Email 1: "Need a landing page"
    │   ├── Create project: ~/ai-projects/landing-page-john-smith/
    │   ├── Generate React landing page template
    │   └── Save project metadata
    │
    ├── Email 2: "Build a todo app"
    │   ├── Create project: ~/ai-projects/todo-app-jane-doe/
    │   ├── Generate full todo app
    │   └── Save project metadata
    │
    └── Email 3: "Create a dashboard"
        ├── Create project: ~/ai-projects/dashboard-acme-corp/
        ├── Generate admin dashboard
        └── Save project metadata

    [Module 3: Computer Use - Email Replies]
    For each client:
    ├── Compose reply:
    │   "Hi [Name],
    │    
    │    Thanks for reaching out! I've started work on your [project].
    │    I'll have an initial version ready for review within 24 hours.
    │    
    │    You can check progress at: [dev server URL]
    │    
    │    Best regards"
    │
    ├── Send email (with confirmation)
    └── Mark original as read

[Final Report]
└── Voice: "I found 3 client requests, created projects for each, 
            and sent confirmation emails. All projects are ready for 
            development in the ai-projects folder."
```

#### Safety Checks
- **Email confirmation:** "Found 3 client emails. Create projects and reply?" → User: "Yes"
- **Draft preview:** Show email drafts before sending
- **Rollback:** Can undo if user says "cancel"

#### Time: ~4 minutes (automated workflow)

---

## Summary Table

| Workflow Type | Example | Time | Modules Used |
|---------------|---------|------|--------------|
| Simple Script | HackerNews scraper | 15s | Voice, Code Gen |
| Data Processing | CSV analyzer | 20s | Code Gen, File Manager |
| Simple App | Todo app | 22s | App Builder |
| Full App | Recipe app | 45s | App Builder, Voice |
| Refactoring | Extract component | 12s | Code Editor |
| Add Feature | Export CSV | 8s | Code Editor |
| Browser - Extract | Gmail invoices | 3min | Computer Use, Vision |
| Browser - Fill | Contact form | 15s | Computer Use, Vision |
| Browser - Scrape | Amazon search | 45s | Computer Use, Vision |
| Full Cycle | Voice→App→Deploy | 5min | All modules |
| Multi-Module | Email→Projects→Reply | 4min | Computer Use, App Builder |

---

## Key Takeaways

### What Makes These Workflows Powerful

1. **Natural Language Input**
   - No need to know React syntax
   - Just describe what you want
   - System handles implementation details

2. **Context Awareness**
   - Remembers project structure
   - Understands related files
   - Maintains coding style consistency

3. **Multi-Step Execution**
   - Breaks down complex tasks
   - Handles errors gracefully
   - Provides progress updates

4. **Safety & Verification**
   - Confirmation prompts for critical actions
   - Screenshot logging for audit
   - Dry-run mode available

5. **Speed**
   - Simple tasks: <30 seconds
   - Full apps: <60 seconds
   - Complex workflows: <5 minutes

### Limitations (Honest Assessment)

**Current System Cannot:**
- ❌ Handle extremely complex multi-file refactoring (>50 files)
- ❌ Understand proprietary/undocumented APIs
- ❌ Generate production-grade code without review
- ❌ Automate tasks requiring CAPTCHAs
- ❌ Handle ambiguous requirements without clarification

**Mitigation:**
- Use cloud fallback (Claude) for complex tasks
- Provide clear, specific instructions
- Review generated code before deploying
- Use confirmation prompts for critical actions

---

## User Quotes (Projected)

> "I described an app idea over voice and had a working prototype in under a minute. This is game-changing." - Beta Tester

> "The refactoring suggestions are surprisingly good. It caught patterns I didn't even realize I was repeating." - Developer

> "Automating my invoice downloads saves me 30 minutes every week. And it's all local, so no privacy concerns." - Freelancer

---

**Document Status:** Complete  
**Last Updated:** April 19, 2026  
**Version:** 1.0
