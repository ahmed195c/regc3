import React, { useState, useEffect } from "react";
import axios from "axios";

function LogsComponent() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
    totalPages: 0,
    totalCount: 0,
  });

  // Filters
  const [filters, setFilters] = useState({
    inUse: "",
    carNumber: "",
    employeeNumber: "",
  });

  const fetchLogs = async () => {
    setLoading(true);
    setError(null);

    try {
      const { page, pageSize } = pagination;
      const { inUse, carNumber, employeeNumber } = filters;

      // Build URL with query parameters
      const params = new URLSearchParams();
      params.append("page", page);
      params.append("page_size", pageSize);

      if (inUse !== "") {
        params.append("in_use", inUse);
      }

      if (carNumber) {
        params.append("car_number", carNumber);
      }

      if (employeeNumber) {
        params.append("employee_number", employeeNumber);
      }

      // Replace with your API URL
      const response = await axios.get(
        `http://192.168.50.6:8000/api/logs/?${params.toString()}`
      );

      setLogs(response.data.results);
      setPagination((prev) => ({
        ...prev,
        totalPages: response.data.pagination.total_pages,
        totalCount: response.data.pagination.total_count,
      }));
    } catch (err) {
      setError(
        "Error fetching data from API. Please check your network connection or CORS settings."
      );
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, [pagination.page, pagination.pageSize]);

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePageChange = (newPage) => {
    setPagination((prev) => ({
      ...prev,
      page: newPage,
    }));
  };

  const applyFilters = () => {
    setPagination((prev) => ({
      ...prev,
      page: 1, // Reset to first page when applying new filters
    }));
    fetchLogs();
  };

  return (
    <div className="logs-container">
      <h2>Vehicle Logs</h2>

      <div className="filters">
        <div className="filter-row">
          <div className="filter-group">
            <label>Status:</label>
            <select
              name="inUse"
              value={filters.inUse}
              onChange={handleFilterChange}
            >
              <option value="">All</option>
              <option value="true">In Use</option>
              <option value="false">Not In Use</option>
            </select>
          </div>

          <div className="filter-group">
            <label>Car Number:</label>
            <input
              type="text"
              name="carNumber"
              value={filters.carNumber}
              onChange={handleFilterChange}
              placeholder="Search by car number"
            />
          </div>

          <div className="filter-group">
            <label>Employee Number:</label>
            <input
              type="text"
              name="employeeNumber"
              value={filters.employeeNumber}
              onChange={handleFilterChange}
              placeholder="Search by employee number"
            />
          </div>

          <button onClick={applyFilters}>Apply Filters</button>
        </div>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : error ? (
        <div className="error-message">{error}</div>
      ) : (
        <>
          <table className="logs-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Car Number</th>
                <th>Employee Name</th>
                <th>Employee Number</th>
                <th>Status</th>
                <th>Taken Date</th>
                <th>Return Date</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {logs.map((log) => (
                <tr key={log.id}>
                  <td>{log.id}</td>
                  <td>{log.car.carNumber}</td>
                  <td>{log.employee.ceoName}</td>
                  <td>{log.employee.ceoNumber}</td>
                  <td>{log.carIsInUse ? "In Use" : "Returned"}</td>
                  <td>{log.taken_date}</td>
                  <td>{log.return_date || "-"}</td>
                  <td>{log.carNote || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="pagination">
            <button
              disabled={pagination.page <= 1}
              onClick={() => handlePageChange(pagination.page - 1)}
            >
              Previous
            </button>

            <span>
              Page {pagination.page} of {pagination.totalPages}
            </span>

            <button
              disabled={pagination.page >= pagination.totalPages}
              onClick={() => handlePageChange(pagination.page + 1)}
            >
              Next
            </button>

            <span className="total-records">
              Total Records: {pagination.totalCount}
            </span>
          </div>
        </>
      )}
    </div>
  );
}

export default LogsComponent;
