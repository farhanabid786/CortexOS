import React from 'react';

interface MarkdownViewerProps {
  content: string;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  if (!content) return <div className="text-slate-500 italic">No blueprint details populated.</div>;

  // Custom simple line-by-line markdown renderer to ensure 100% dependency-free robustness
  const parseMarkdown = (text: string) => {
    const lines = text.split('\n');
    const elements: React.ReactNode[] = [];
    let currentTable: { headers: string[]; rows: string[][] } | null = null;
    let inCodeBlock = false;
    let codeBlockContent: string[] = [];

    const formatInline = (str: string) => {
      // We can convert to React nodes by splitting
      const parts: React.ReactNode[] = [];
      let lastIndex = 0;
      
      // Simple regex parser
      const combinedRegex = /(\*\*.*?\*\*|`.*?`)/g;
      let match;
      
      while ((match = combinedRegex.exec(str)) !== null) {
        // Add preceding text
        if (match.index > lastIndex) {
          parts.push(str.substring(lastIndex, match.index));
        }
        
        const token = match[0];
        if (token.startsWith('**') && token.endsWith('**')) {
          parts.push(<strong key={match.index} className="text-white font-semibold">{token.slice(2, -2)}</strong>);
        } else if (token.startsWith('`') && token.endsWith('`')) {
          parts.push(<code key={match.index} className="bg-slate-900 border border-slate-800 text-cyan-300 px-1 py-0.5 rounded font-mono text-xs">{token.slice(1, -1)}</code>);
        }
        
        lastIndex = combinedRegex.lastIndex;
      }
      
      if (lastIndex < str.length) {
        parts.push(str.substring(lastIndex));
      }
      
      return parts.length > 0 ? parts : str;
    };

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Code blocks
      if (line.trim().startsWith('```')) {
        if (inCodeBlock) {
          inCodeBlock = false;
          elements.push(
            <pre key={`code-${i}`} className="bg-slate-950/80 border border-slate-800/80 p-4 rounded-xl font-mono text-xs text-slate-300 overflow-x-auto my-4">
              <code>{codeBlockContent.join('\n')}</code>
            </pre>
          );
          codeBlockContent = [];
        } else {
          inCodeBlock = true;
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlockContent.push(line);
        continue;
      }

      // Tables
      if (line.trim().startsWith('|')) {
        const cells = line.split('|').map(c => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        
        // Skip separator line |---|---|
        if (cells.every(c => c.startsWith('-'))) {
          continue;
        }

        if (!currentTable) {
          currentTable = { headers: cells, rows: [] };
        } else {
          currentTable.rows.push(cells);
        }
        continue;
      } else {
        if (currentTable) {
          elements.push(
            <div key={`table-${i}`} className="overflow-x-auto my-6 border border-slate-800 rounded-xl">
              <table className="min-w-full divide-y divide-slate-800 text-sm">
                <thead className="bg-slate-900/60">
                  <tr>
                    {currentTable.headers.map((h, idx) => (
                      <th key={idx} className="px-4 py-3 text-left font-bold text-slate-300 tracking-wider">
                        {formatInline(h)}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 bg-transparent">
                  {currentTable.rows.map((row, rIdx) => (
                    <tr key={rIdx} className="hover:bg-white/5 transition-colors">
                      {row.map((cell, cIdx) => (
                        <td key={cIdx} className="px-4 py-3 text-slate-300 whitespace-nowrap">
                          {formatInline(cell)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          );
          currentTable = null;
        }
      }

      // Headings
      if (line.startsWith('# ')) {
        elements.push(<h1 key={i} className="text-3xl font-extrabold text-white mt-8 mb-4 border-b border-slate-800 pb-2">{formatInline(line.slice(2))}</h1>);
      } else if (line.startsWith('## ')) {
        elements.push(<h2 key={i} className="text-2xl font-bold text-white mt-6 mb-3">{formatInline(line.slice(3))}</h2>);
      } else if (line.startsWith('### ')) {
        elements.push(<h3 key={i} className="text-xl font-semibold text-cyan-400 mt-4 mb-2">{formatInline(line.slice(4))}</h3>);
      }
      // Lists
      else if (line.trim().startsWith('- ') || line.trim().startsWith('* ')) {
        elements.push(
          <ul key={i} className="list-disc pl-6 space-y-1 my-2 text-slate-300 text-sm">
            <li>{formatInline(line.trim().slice(2))}</li>
          </ul>
        );
      } else if (/^\d+\.\s/.test(line.trim())) {
        const contentStr = line.trim().replace(/^\d+\.\s/, '');
        elements.push(
          <ol key={i} className="list-decimal pl-6 space-y-1 my-2 text-slate-300 text-sm">
            <li>{formatInline(contentStr)}</li>
          </ol>
        );
      }
      // Normal Paragraphs
      else if (line.trim() !== '') {
        elements.push(<p key={i} className="text-slate-300 text-sm leading-relaxed my-3">{formatInline(line)}</p>);
      }
    }

    return elements;
  };

  return <div className="space-y-2 select-text">{parseMarkdown(content)}</div>;
};
export default MarkdownViewer;
