import React from 'react';

interface DataTableProps<T> {
  title: string;
  columns: string[];
  data: T[];
  renderRow: (item: T, index: number) => React.ReactNode;
}

export function DataTable<T>({ title, columns, data, renderRow }: DataTableProps<T>) {
  return (
    <div className="table-container">
      <h2 className="table-title">{title}</h2>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col, idx) => (
                <th key={idx}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((item, idx) => renderRow(item, idx))}
            {data.length === 0 && (
              <tr>
                <td colSpan={columns.length} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                  No data available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
