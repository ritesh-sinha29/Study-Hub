function trimCommonIndentation(lines: string[]): string[] {
  if (lines.length === 0) return [];
  
  let minIndent = Infinity;
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    if (line.trim() === '') continue;
    const match = line.match(/^(\s*)/);
    if (match) {
      const indent = match[1].length;
      if (indent < minIndent) {
        minIndent = indent;
      }
    }
  }

  if (minIndent === Infinity) {
    return lines.map(l => l.trim());
  }

  return lines.map((line, idx) => {
    if (idx === 0) return line.trim();
    if (line.trim() === '') return '';
    
    if (line.startsWith(' '.repeat(minIndent))) {
      return line.substring(minIndent);
    }
    return line.trim();
  });
}

function isDivider(line: string): boolean {
  if (!line) return false;
  return line.trim().match(/^#\s*[=\-]{5,}/) !== null;
}

/** Detects box-drawing / ASCII-art diagram lines */
function isAsciiDiagramLine(text: string): boolean {
  const trimmed = text.trim();
  // If it starts with a list bullet or numbered bullet, it's text, not a diagram
  if (/^[-*+]\s+/.test(trimmed) || /^\d+\.\s+/.test(trimmed)) return false;

  // Contains Unicode box-drawing characters
  if (/[\u2500-\u257F\u2580-\u259F]/.test(text)) return true;
  // Heavy horizontal rule lines like ━━━━━━━
  if (/^[\s]*[━─═]{4,}/.test(text)) return true;
  // Lines that contain diagram connectors/arrows like -->, ==>, ->, ⇄
  if (/\s*([─═\-]{2,}>|<[─═\-]{2,}|\u21c4|\u21e8|\u21e6|\u21cc)/.test(text)) return true;
  // Lines that are purely box art: lots of │ ┌ └ ─ ┐ ┘ spaces
  if (/^[\s│┌└─┐┘┤├┬┴┼╔╗╚╝║═\s\-\=\>\<]{6,}$/.test(text)) return true;
  // Standalone vertical flow arrows (▼ ▲ ↓ ↑) on a line (possibly with spaces)
  if (/^\s*[▼▲↓↑]\s*$/.test(text)) return true;
  // Lines with inline ← → ▼ ▲ surrounded by non-box content (flow labels)
  if (/[▼▲↓↑←→⟵⟶⇐⇒]/.test(text)) return true;
  return false;
}

/** Detects markdown pipe-table rows (lines starting/containing | col | col) */
function isMarkdownTableLine(text: string): boolean {
  const t = text.trim();
  // Must start with | and have at least two | separators
  return t.startsWith('|') && (t.match(/\|/g) || []).length >= 2;
}

/** Tries to convert a box-drawing ASCII table (using │, ┌, ├, etc.) to a standard Markdown table */
function tryConvertBoxTable(lines: string[]): string[] | null {
  const hasColumns = lines.some(l => l.includes('│') || l.includes('║'));
  if (!hasColumns) return null;

  // Flowchart/diagram detection: If lines contain standalone flow arrows (▼, ▲, ↓, ──►, -->)
  // or connector links, it's a visual flowchart, not a structured tabular block.
  const hasFlowElements = lines.some(line => {
    const trimmed = line.trim();
    if (/[─═\-]{2,}>|<[─═\-]{2,}/.test(trimmed)) return true;
    if (/\b(?:[a-zA-Z0-9_\-\s]+)\s*(?:[─═\-]{2,}>|-->)\s*(?:[a-zA-Z0-9_\-\s]+)\b/.test(trimmed)) return true;
    // Standalone vertical arrow on its own line — unmistakable flowchart indicator
    if (/^\s*[▼▲↓↑]\s*$/.test(trimmed)) return true;
    // Inline arrows mixed with labels (e.g. "[node] ← LLM decides")
    if (/[▼▲↓↑←→]/.test(trimmed)) return true;
    // Check if one of the columns is just an arrow pointing down/up
    if (line.includes('│') || line.includes('║')) {
      const parts = line.split(/[│║]/).map(p => p.trim());
      if (parts.some(p => p === '▼' || p === '▲' || p === '↓' || p === '↑' || p === '→' || p === '←')) {
        return true;
      }
    }
    return false;
  });

  if (hasFlowElements) return null;

  const tableRows: string[] = [];
  let maxCols = 0;

  for (const line of lines) {
    let cleanLine = line.trim();
    if (!cleanLine) continue;

    // Check if the line is just a decorative boundary/border line (e.g. ┌────┐ or └────┘)
    const isBoundary = /^[┌┐└┘╔╗╚╝╓╢╙╒╞╘═─┬┼┴╦╬╩╪╫╬═─\s]+$/.test(cleanLine);
    if (isBoundary) {
      // Intersections are used to detect column boundaries
      if (cleanLine.includes('┼') || cleanLine.includes('╬') || cleanLine.includes('╪') || cleanLine.includes('┬') || cleanLine.includes('├')) {
        if (maxCols > 0) {
          tableRows.push('|' + ' --- |'.repeat(maxCols));
        }
      }
      continue;
    }

    // Strip outer borders if they exist (e.g. starting and ending with box vertical lines)
    if (cleanLine.startsWith('│') && cleanLine.endsWith('│')) {
      cleanLine = cleanLine.substring(1, cleanLine.length - 1).trim();
    } else if (cleanLine.startsWith('║') && cleanLine.endsWith('║')) {
      cleanLine = cleanLine.substring(1, cleanLine.length - 1).trim();
    }

    // Split line by columns
    const cols = cleanLine.split(/[│║|]/).map(c => c.trim());
    if (cols.length < 2) {
      continue; // Skip title headers or empty rows in box
    }

    // Check if the row itself is a separator line (all hyphens or double lines)
    const isSeparatorRow = cols.every(col => /^[─═\-\s]+$/.test(col));
    if (isSeparatorRow) {
      tableRows.push('|' + ' --- |'.repeat(cols.length));
    } else {
      if (tableRows.length > 0) {
        // Data row: Bold the first cell only if it's non-empty (avoids "****" from empty │ cells)
        const firstCell = cols[0].trim();
        const boldedFirst = firstCell ? `**${firstCell}**` : '';
        const restCols = cols.slice(1);
        tableRows.push('| ' + [boldedFirst, ...restCols].join(' | ') + ' |');
      } else {
        // Header row: Keep as is
        tableRows.push('| ' + cols.join(' | ') + ' |');
      }
      maxCols = Math.max(maxCols, cols.length);
    }
  }

  // A valid table needs at least a header and some data rows
  if (tableRows.length >= 2 && maxCols >= 2) {
    // Keep only one separator row, right after the first row
    const cleanTable: string[] = [];
    let addedSep = false;

    for (let i = 0; i < tableRows.length; i++) {
      const row = tableRows[i];
      const isSep = /^\|[-:\s|]+\|$/.test(row.trim());

      if (isSep) {
        if (!addedSep && cleanTable.length > 0) {
          cleanTable.push(row);
          addedSep = true;
        }
      } else {
        cleanTable.push(row);
      }
    }

    // If no separator row was found, inject one after the header
    const hasSep = cleanTable.some(row => /^\|[-:\s|]+\|$/.test(row.trim()));
    if (!hasSep && cleanTable.length >= 1) {
      const sep = '|' + ' --- |'.repeat(maxCols);
      cleanTable.splice(1, 0, sep);
    }

    return cleanTable;
  }

  return null;
}

function isCodeLine(text: string): boolean {
  const t = text.trim();
  if (t === '') return false;
  
  return t.startsWith('@') || 
         t.startsWith('def ') || 
         t.startsWith('async def ') || 
         t.startsWith('import ') || 
         t.startsWith('from ') || 
         t.startsWith('class ') ||
         t.startsWith('return ') ||
         t.startsWith('yield ') ||
         t.startsWith('pass') ||
         t.startsWith('assert ') ||
         t.includes(' = Depends(') ||
         t.includes(' = await ') ||
         t.startsWith('app = FastAPI(') ||
         t.startsWith('uvicorn.run(');
}

function replaceOutsideBackticks(text: string, regex: RegExp, replacement: string): string {
  const parts = text.split('`');
  for (let i = 0; i < parts.length; i += 2) {
    parts[i] = parts[i].replace(regex, replacement);
  }
  return parts.join('`');
}

function formatInlineCode(text: string): string {
  let formatted = text;
  formatted = replaceOutsideBackticks(formatted, /\{"[^"]+"\s*:\s*[^}]*\}/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\{'[^']+'\s*:\s*[^}]*\}/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\b(Annotated|List|Dict|Tuple|Set|Union|Optional)\[[^\]]+\]/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\b([a-zA-Z0-9_]+\["[^"]+"\])/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\b([a-zA-Z0-9_]+\('[^']+'\))/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\b([a-zA-Z0-9_]+\("[^"]+"\))/g, '`$&`');
  formatted = replaceOutsideBackticks(formatted, /\b([a-zA-Z0-9]+_[a-zA-Z0-9_]*(?:\.[a-zA-Z0-9]+)?)\b/g, '`$1`');
  return formatted;
}

function processTextLines(lines: string[]): string {
  if (lines.length <= 1) {
    return lines.map(line => formatInlineCode(line)).join('\n').trim();
  }

  const hasListOrStructure = lines.some((line, index) => {
    const trimmed = line.trim();
    if (!trimmed) return false;
    if (/^[-*+]\s+/.test(trimmed) || /^\d+\.\s+/.test(trimmed)) return true;
    if (/^[A-Za-z0-9_-]+\s*=\s*/.test(trimmed)) return true;
    if (/^(Node|Step|Task|Stage|State holds|Conditional edges|Benefit|Routing|Input|Output|DEFAULT REDUCER|CUSTOM REDUCER|METHOD [A-Z]|User asks|User says|Agent calls|Reads result|Code|Edges|Condition|Result)\s*\d*:\s*/i.test(trimmed)) return true;
    if (index > 0) {
      const firstLineIndent = lines[0].match(/^(\s*)/)?.[1].length || 0;
      const currentLineIndent = line.match(/^(\s*)/)?.[1].length || 0;
      if (currentLineIndent > firstLineIndent + 1) return true;
    }
    return false;
  });

  if (!hasListOrStructure) {
    return lines.map(line => formatInlineCode(line)).join('\n').trim();
  }

  return lines.map((line, idx) => {
    const trimmed = line.trim();
    if (!trimmed) return '';

    let processedLine = line;
    const labelMatch = line.match(/^(\s*)(Node\s*\d+|Step\s*\d+|State holds|Conditional edges|Benefit|Routing|Input|Output|DEFAULT REDUCER|CUSTOM REDUCER|METHOD\s+[A-Z]|User asks\s*\d*|User says\s*\d*|Agent calls\s*\d*|Reads result\s*\d*|Code|Edges|Condition|Result\s*\d*)(\s*\([^)]*\))?(:\s*.*)/i);
    
    if (labelMatch) {
      const indent = labelMatch[1] || '   ';
      const label = labelMatch[2];
      const parens = labelMatch[3] || '';
      const rest = labelMatch[4];
      processedLine = `${indent}- **${label}${parens}**${formatInlineCode(rest)}`;
    } else {
      const bulletMatch = line.match(/^(\s*[-*+]\s+|\s*\d+\.\s+)(.*)/);
      if (bulletMatch) {
        processedLine = bulletMatch[1] + formatInlineCode(bulletMatch[2]);
      } else {
        processedLine = formatInlineCode(line);
      }
    }

    if (idx < lines.length - 1 && !/^(\s*[-*+]\s+|\s*\d+\.\s+)/.test(line)) {
      return processedLine + '  ';
    }
    return processedLine;
  }).join('\n');
}

export function parsePythonToMarkdown(rawContent: string, pageTitle: string): string {
  let content = rawContent.replace(/\r\n/g, '\n');

  // Strip outermost ```python and ``` wrapper if present
  const pythonWrapperStart = /^#\s+[^\n]+\n\n```python\n/;
  if (content.match(pythonWrapperStart)) {
    content = content.replace(pythonWrapperStart, '');
    content = content.replace(/\n```\s*$/, '');
  }

  const lines = content.split('\n');
  const blocks: Array<{ type: 'heading' | 'text' | 'text_code' | 'code'; level?: number; text?: string; lines?: string[] }> = [];
  const qas: Array<{ id: string; question: string; answerLines: string[] }> = [];

  let currentBlock: any = null;
  let currentQA: any = null;
  let inQASection = false;

  function finishCurrentBlock() {
    if (currentBlock) {
      blocks.push(currentBlock);
      currentBlock = null;
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const trimmed = line.trim();

    // Check Q&A section
    const upperTrimmed = trimmed.toUpperCase();
    if (trimmed.startsWith('#') && (
      upperTrimmed.includes('MNC INTERVIEW') || 
      upperTrimmed.includes('INTERVIEW PREPARATION') || 
      upperTrimmed.includes('INTERVIEW QUESTIONS') || 
      upperTrimmed.includes('INTERVIEW Q&A')
    )) {
      inQASection = true;
      finishCurrentBlock();
      continue;
    }

    if (inQASection) {
      if (trimmed.startsWith('#')) {
        const qMatch = line.match(/^#\s*(Q\d+)\.\s*(.*)/);
        if (qMatch) {
          if (currentQA) {
            currentQA.answerLines = trimCommonIndentation(currentQA.answerLines);
            qas.push(currentQA);
          }
          currentQA = {
            id: qMatch[1],
            question: qMatch[2].trim(),
            answerLines: []
          };
          continue;
        }

        const aMatch = line.match(/^#\s*A:\s*(.*)/);
        if (aMatch && currentQA) {
          currentQA.answerLines.push(aMatch[1].trim());
          continue;
        }

        if (currentQA) {
          if (currentQA.answerLines.length === 0) {
            // Continuation of the question
            const cleanQuestionPart = line.replace(/^#\s*/, '').trim();
            currentQA.question += ' ' + cleanQuestionPart;
          } else {
            // Continuation of the answer
            let cleanLine = line.replace(/^#\s?/, '');
            cleanLine = cleanLine.replace(/^(\s*)#\s?/, '$1');
            currentQA.answerLines.push(cleanLine);
          }
        }
      }
      continue;
    }

    // 1. Divider lines (=====, -----, ━━━━━ in comments)
    if (isDivider(line)) {
      finishCurrentBlock();
      continue;
    }
    // Heavy box dividers inside comment body: # ━━━━━━━━━━━━
    if (line.startsWith('#') && /^#\s*[\u2500\u2501\u2550]{4,}/.test(line)) {
      finishCurrentBlock();
      continue;
    }

    // 2. Subheadings like # --- WHAT IS ... ---
    const subheadingMatch = line.match(/^#\s*---\s*(.*?)\s*---/);
    if (subheadingMatch) {
      finishCurrentBlock();
      blocks.push({
        type: 'heading',
        level: 2,
        text: subheadingMatch[1].trim()
      });
      continue;
    }

    // 2b. SECTION N — HEADING TITLE pattern
    const sectionMatch = line.match(/^#\s*SECTION\s+\d+\s*[\u2014\u2013-]+\s*(.+)/);
    if (sectionMatch) {
      finishCurrentBlock();
      blocks.push({
        type: 'heading',
        level: 2,
        text: sectionMatch[1].trim()
      });
      continue;
    }

    // 3. Comment lines
    if (line.startsWith('#')) {
      const textContent = line.startsWith('# ') ? line.substring(2) : line.substring(1);

      if (textContent.includes('REAL-LIFE USE CASES') || textContent.includes('REAL-WORLD USE CASES')) {
        finishCurrentBlock();
        blocks.push({
          type: 'heading',
          level: 2,
          text: 'Real-World Use Cases'
        });
        continue;
      }

      if (textContent.includes('HOW TO RUN THIS FILE') || textContent.includes('QUICK SUMMARY')) {
        finishCurrentBlock();
        blocks.push({
          type: 'heading',
          level: 2,
          text: textContent.replace(/---/g, '').trim()
        });
        continue;
      }

      // Surrounded by dividers
      const prevLine = lines[i - 1];
      const nextLine = lines[i + 1];
      if (isDivider(prevLine) && isDivider(nextLine)) {
        finishCurrentBlock();
        blocks.push({
          type: 'heading',
          level: 2,
          text: textContent.trim()
        });
        continue;
      }

      if (textContent.trim() === '') {
        if (currentBlock) {
          if (currentBlock.type === 'text_code') {
            currentBlock.lines.push('');
          } else if (currentBlock.type === 'text') {
            finishCurrentBlock();
          }
        }
        continue;
      }

      if (isCodeLine(textContent)) {
        if (currentBlock && currentBlock.type === 'text_code') {
          currentBlock.lines.push(textContent);
        } else {
          finishCurrentBlock();
          currentBlock = {
            type: 'text_code',
            lines: [textContent]
          };
        }
      } else {
        if (currentBlock && currentBlock.type === 'text') {
          currentBlock.lines.push(textContent);
        } else {
          finishCurrentBlock();
          currentBlock = {
            type: 'text',
            lines: [textContent]
          };
        }
      }
      continue;
    }

    // 4. Empty lines
    if (trimmed === '') {
      if (currentBlock) {
        if (currentBlock.type === 'code') {
          currentBlock.lines.push('');
        } else if (currentBlock.type === 'text' || currentBlock.type === 'text_code') {
          finishCurrentBlock();
        }
      }
      continue;
    }

    // 5. Normal Code lines
    if (currentBlock && currentBlock.type === 'code') {
      currentBlock.lines.push(line);
    } else {
      finishCurrentBlock();
      currentBlock = {
        type: 'code',
        lines: [line]
      };
    }
  }

  finishCurrentBlock();
  if (currentQA) {
    currentQA.answerLines = trimCommonIndentation(currentQA.answerLines);
    qas.push(currentQA);
  }

  // Build Markdown
  let md = `# ${pageTitle}\n\n`;

  let skippedFirstHeading = false;
  for (const block of blocks) {
    if (block.type === 'heading') {
      if (!skippedFirstHeading) {
        skippedFirstHeading = true;
        continue;
      }
      md += `${'#'.repeat(block.level || 2)} ${block.text}\n\n`;
    } else if (block.type === 'text' && block.lines) {
      // Split text blocks into sub-groups: normal text, ascii diagrams, markdown tables
      const subGroups: Array<{ kind: 'text' | 'diagram' | 'table'; lines: string[] }> = [];
      let currentGroup: { kind: 'text' | 'diagram' | 'table'; lines: string[] } | null = null;

      for (let idx = 0; idx < block.lines.length; idx++) {
        const tline = block.lines[idx];
        let kind: 'text' | 'diagram' | 'table' = 'text';
        if (isAsciiDiagramLine(tline)) kind = 'diagram';
        else if (isMarkdownTableLine(tline)) kind = 'table';

        // Bidirectional lookahead: if this text line is short (a label, not a paragraph)
        // merge it into the diagram group using either forward or backward context.
        // Forward: a diagram line appears within the next 3 lines → start/extend diagram.
        // Backward: we're already inside a diagram group → keep trailing labels in the box.
        if (kind === 'text') {
          const trimmedLine = tline.trim();
          const isLikelyLabel = trimmedLine.length > 0 && trimmedLine.length <= 80;

          if (isLikelyLabel) {
            // Forward lookahead: diagram follows soon
            let hasDiagramAhead = false;
            for (let j = 1; j <= 3; j++) {
              if (idx + j < block.lines.length && isAsciiDiagramLine(block.lines[idx + j])) {
                hasDiagramAhead = true;
                break;
              }
            }
            // Backward context: already inside a diagram group
            const inDiagramGroup = currentGroup !== null && currentGroup.kind === 'diagram';

            if (hasDiagramAhead || inDiagramGroup) {
              kind = 'diagram';
            }
          }
        }

        if (!currentGroup || currentGroup.kind !== kind) {
          if (currentGroup) subGroups.push(currentGroup);
          currentGroup = { kind, lines: [tline] };
        } else {
          currentGroup.lines.push(tline);
        }
      }
      if (currentGroup) subGroups.push(currentGroup);

      for (const sg of subGroups) {
        let sgText = '';
        if (sg.kind === 'diagram') {
          let start = 0;
          while (start < sg.lines.length && sg.lines[start].trim() === '') start++;
          let end = sg.lines.length - 1;
          while (end >= start && sg.lines[end].trim() === '') end--;
          if (start <= end) {
            const activeLines = sg.lines.slice(start, end + 1);
            sgText = trimCommonIndentation(activeLines).map(line => line.trimEnd()).join('\n');
          }
        } else {
          sgText = sg.lines.join('\n').trim();
        }
        if (!sgText) continue;

        if (sg.kind === 'diagram') {
          const convertedTable = tryConvertBoxTable(sg.lines);
          if (convertedTable) {
            md += convertedTable.join('\n') + '\n\n';
          } else {
            md += '```text\n' + sgText + '\n```\n\n';
          }
        } else if (sg.kind === 'table') {
          // Ensure there is a GFM separator row after the first line
          const tableLines = sg.lines.filter(l => l.trim());
          // Check if separator row already exists
          const hasSeparator = tableLines.some(l => /^\|[-:\s|]+\|$/.test(l.trim()));
          if (!hasSeparator && tableLines.length >= 1) {
            // Build a separator based on column count of first row
            const cols = (tableLines[0].match(/\|/g) || []).length - 1;
            const sep = '|' + ' --- |'.repeat(Math.max(cols, 1));
            tableLines.splice(1, 0, sep);
          }
          md += tableLines.join('\n') + '\n\n';
        } else {
          md += `${processTextLines(sg.lines)}\n\n`;
        }
      }
    } else if (block.type === 'text_code' && block.lines) {
      const codeText = block.lines.join('\n').trim();
      if (codeText) {
        md += '```python\n' + codeText + '\n```\n\n';
      }
    } else if (block.type === 'code' && block.lines) {
      const codeText = block.lines.join('\n').trim();
      if (codeText) {
        md += '```python\n' + codeText + '\n```\n\n';
      }
    }
  }

  if (qas.length > 0) {
    md += `<Questions>\n`;
    for (const qa of qas) {
      const answer = qa.answerLines.join('\n').trim();
      md += `<Question id="${qa.id}" title="${qa.question}">\n${answer}\n</Question>\n`;
    }
    md += `</Questions>\n`;
  }

  return md;
}
