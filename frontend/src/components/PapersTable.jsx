import React, { useState } from 'react';

const PapersTable = ({ papers }) => {
  const [searchTerm, setSearchTerm] = useState('');

  if (!papers || papers.length === 0) {
    return (
      <div className="card">
        <p className="text-gray-500 text-center py-8">No publications found</p>
      </div>
    );
  }

  const filteredPapers = papers.filter((paper) =>
    paper.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    paper.authors.some((author) => author.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="card">
        <input
          type="text"
          placeholder="Search by title or author..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field"
        />
      </div>

      {/* Results Count */}
      <div className="text-sm text-gray-600">
        Showing {filteredPapers.length} of {papers.length} publications
      </div>

      {/* Papers List */}
      <div className="space-y-4">
        {filteredPapers.map((paper, index) => (
          <div key={paper.pmid || index} className="card hover:shadow-lg transition-shadow">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {paper.title}
            </h3>

            <div className="text-sm text-gray-600 mb-3">
              {paper.authors && paper.authors.length > 0 && (
                <p className="mb-1">
                  <span className="font-medium">Authors:</span>{' '}
                  {paper.authors.slice(0, 5).join(', ')}
                  {paper.authors.length > 5 && ` et al. (${paper.authors.length} authors)`}
                </p>
              )}

              <div className="flex flex-wrap gap-3">
                {paper.journal && (
                  <span>
                    <span className="font-medium">Journal:</span> {paper.journal}
                  </span>
                )}
                {paper.publication_date && (
                  <span>
                    <span className="font-medium">Date:</span> {paper.publication_date}
                  </span>
                )}
                {paper.pmid && (
                  <span>
                    <span className="font-medium">PMID:</span>{' '}
                    <a
                      href={paper.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-primary-600 hover:underline"
                    >
                      {paper.pmid}
                    </a>
                  </span>
                )}
              </div>
            </div>

            {paper.abstract && (
              <div className="text-sm text-gray-700">
                <p className="line-clamp-3">{paper.abstract}</p>
              </div>
            )}

            {paper.keywords && paper.keywords.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1">
                {paper.keywords.slice(0, 5).map((keyword, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PapersTable;
