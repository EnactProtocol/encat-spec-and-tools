### Common Errors

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| `INVALID_SCHEMA` | Capability definition doesn't match schema | Validate against schema, check required fields |
| `DEPENDENCY_NOT_FOUND` | Missing runtime dependency | Add required package to dependencies section |
| `TASK_EXECUTION_TIMEOUT` | Task exceeded timeout limit | Increase timeout in resources or optimize task |
| `ENVIRONMENT_VARIABLE_MISSING` | Required env var not provided | Check env var configuration in execution context |
| `PERMISSION_DENIED` | Insufficient permissions | Check required permissions and authentication |
| `INVALID_HASH` | Invalid Capability Hash | Your Capability may be malicious |