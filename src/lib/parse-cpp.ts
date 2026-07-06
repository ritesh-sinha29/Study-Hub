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
  return line.trim().match(/^\/\/ \s*[=\-]{5,}/) !== null;
}

function isCodeLine(text: string): boolean {
  const t = text.trim();
  if (t === '') return false;
  
  return t.startsWith('#include') || 
         t.startsWith('using namespace') || 
         t.startsWith('int main(') || 
         t.startsWith('std::') || 
         t.startsWith('cout ') || 
         t.startsWith('cin ') ||
         t.startsWith('struct ') ||
         t.startsWith('class ') ||
         t.startsWith('template') ||
         t.startsWith('public:') ||
         t.startsWith('private:') ||
         t.startsWith('void ') ||
         t.startsWith('int ') ||
         t.startsWith('double ') ||
         t.startsWith('float ') ||
         t.startsWith('char ') ||
         t.startsWith('string ') ||
         t.startsWith('bool ') ||
         t.startsWith('if (') ||
         t.startsWith('for (') ||
         t.startsWith('while (') ||
         t.startsWith('switch (') ||
         t.startsWith('case ') ||
         t.startsWith('return ');
}

export function parseCppToMarkdown(rawContent: string, pageTitle: string): string {
  let content = rawContent.replace(/\r\n/g, '\n');

  // Strip outermost ```cpp and ``` wrapper if present
  const cppWrapperStart = /^\/\/\s+[^\n]+\n\n```cpp\n/;
  if (content.match(cppWrapperStart)) {
    content = content.replace(cppWrapperStart, '');
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
    if (trimmed.startsWith('//') && trimmed.includes('MNC INTERVIEW QUESTIONS')) {
      inQASection = true;
      finishCurrentBlock();
      continue;
    }

    if (inQASection) {
      if (trimmed.startsWith('//')) {
        const qMatch = line.match(/^\/\/\s*(?:[^\w\s]+\s*)?(Q\d+)\.\s*(.*)/);
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

        const aMatch = line.match(/^\/\/\s*A:\s*(.*)/);
        if (aMatch && currentQA) {
          currentQA.answerLines.push(aMatch[1].trim());
          continue;
        }

        if (currentQA) {
          if (currentQA.answerLines.length === 0) {
            // Continuation of the question
            const cleanQuestionPart = line.replace(/^\/\/\s*/, '').trim();
            currentQA.question += ' ' + cleanQuestionPart;
          } else {
            // Continuation of the answer
            let cleanLine = line.replace(/^\/\/\s?/, '');
            cleanLine = cleanLine.replace(/^(\s*)\/\/\s?/, '$1');
            currentQA.answerLines.push(cleanLine);
          }
        }
      }
      continue;
    }

    // 1. Divider lines
    if (isDivider(line)) {
      finishCurrentBlock();
      continue;
    }

    // 2. Subheadings like // --- WHAT IS ... ---
    const subheadingMatch = line.match(/^\/\/\s*---\s*(.*?)\s*---/);
    if (subheadingMatch) {
      finishCurrentBlock();
      blocks.push({
        type: 'heading',
        level: 2,
        text: subheadingMatch[1].trim()
      });
      continue;
    }

    // 3. Comment lines
    if (line.startsWith('//')) {
      const textContent = line.startsWith('// ') ? line.substring(3) : line.substring(2);

      if (textContent.includes('REAL-LIFE USE CASES')) {
        finishCurrentBlock();
        blocks.push({
          type: 'heading',
          level: 2,
          text: 'Real-Life Use Cases'
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

  for (const block of blocks) {
    if (block.type === 'heading') {
      md += `${'#'.repeat(block.level || 2)} ${block.text}\n\n`;
    } else if (block.type === 'text' && block.lines) {
      const text = block.lines.join('\n').trim();
      if (text) {
        md += `${text}\n\n`;
      }
    } else if (block.type === 'text_code' && block.lines) {
      const codeText = block.lines.join('\n').trim();
      if (codeText) {
        md += '```cpp\n' + codeText + '\n```\n\n';
      }
    } else if (block.type === 'code' && block.lines) {
      const codeText = block.lines.join('\n').trim();
      if (codeText) {
        md += '```cpp\n' + codeText + '\n```\n\n';
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
