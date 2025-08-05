# CI/CD Pipeline Setup Guide

This guide explains how to set up the GitHub Actions CI/CD pipeline for building and deploying your Flask application to Amazon ECR.

## 🚀 What the Pipeline Does

The CI/CD pipeline automatically:
1. **Tests** your Flask application
2. **Builds** a Docker image with optimizations
3. **Pushes** the image to Amazon ECR
4. **Tags** images with environment, commit SHA, and version tags
5. **Notifies** on deployment status

## 📋 Prerequisites

### 1. AWS Credentials
You need AWS credentials with ECR permissions. Create an IAM user with these policies:
- `AmazonEC2ContainerRegistryFullAccess`
- Or custom policy with ECR permissions

### 2. GitHub Repository Secrets
Add these secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

### 3. ECR Repository
Ensure your ECR repository exists:
```bash
aws ecr create-repository --repository-name my-app --region us-west-2
```

## 🔧 Pipeline Configuration

### Trigger Events
The pipeline runs on:
- **Push** to `main` or `master` branch
- **Pull Request** to `main` or `master` branch (tests only)
- **Manual trigger** with environment selection

### Environment Variables
```yaml
AWS_REGION: us-west-2
ECR_REPOSITORY: my-app
```

### Image Tags
The pipeline creates multiple tags:
- `latest` - Latest successful build
- `{commit-sha}` - Specific commit
- `{environment}` - development/staging/production
- `{version}` - If using git tags

## 🏗️ Build Process

### 1. Testing Phase
- Installs Python dependencies
- Runs unit tests with pytest
- Tests Docker build locally
- Validates application imports

### 2. Build Phase
- Uses multi-stage Docker build
- Optimizes for production
- Implements security best practices
- Uses GitHub Actions cache for speed

### 3. Push Phase
- Authenticates with ECR
- Pushes optimized image
- Creates multiple tags
- Provides deployment feedback

## 🐳 Docker Optimizations

### Multi-stage Build
```dockerfile
# Builder stage - installs dependencies
FROM python:3.11-slim as builder
# ... install dependencies

# Production stage - minimal runtime
FROM python:3.11-slim
# ... copy only what's needed
```

### Security Features
- Non-root user (`appuser`)
- Minimal base image
- Health checks
- Environment isolation

### Performance Features
- Layer caching
- Multi-platform support
- Optimized dependencies
- Production-ready configuration

## 🚀 Usage

### Automatic Deployment
1. Push to `main` branch
2. Pipeline runs automatically
3. Image is built and pushed to ECR
4. Check Actions tab for status

### Manual Deployment
1. Go to Actions → Build and Deploy Flask App to ECR
2. Click "Run workflow"
3. Select environment (development/staging/production)
4. Click "Run workflow"

### Environment Deployment
```bash
# Deploy to development
aws ecs update-service --cluster dev-cluster --service my-app --force-new-deployment

# Deploy to production
aws ecs update-service --cluster prod-cluster --service my-app --force-new-deployment
```

## 📊 Monitoring

### GitHub Actions
- View pipeline status in Actions tab
- Check logs for debugging
- Monitor build times and success rates

### ECR Monitoring
```bash
# List images
aws ecr describe-images --repository-name my-app --region us-west-2

# Check image details
aws ecr describe-images --repository-name my-app --image-ids imageTag=latest
```

## 🔧 Customization

### Environment Variables
Update `.github/workflows/flask-app-ecr.yml`:
```yaml
env:
  AWS_REGION: your-region
  ECR_REPOSITORY: your-repo-name
```

### Build Arguments
Add to Dockerfile:
```dockerfile
ARG BUILD_VERSION
ENV VERSION=$BUILD_VERSION
```

### Additional Tests
Add to `test_app.py`:
```python
def test_custom_endpoint(self):
    response = self.app.get('/custom')
    self.assertEqual(response.status_code, 200)
```

## 🛠️ Troubleshooting

### Common Issues

1. **AWS Credentials Error**
   - Verify IAM permissions
   - Check secret names in GitHub
   - Ensure ECR repository exists

2. **Build Failures**
   - Check Dockerfile syntax
   - Verify requirements.txt
   - Review build logs

3. **Test Failures**
   - Run tests locally first
   - Check Python version compatibility
   - Verify test dependencies

### Debug Commands
```bash
# Test locally
python -m pytest test_app.py -v

# Build locally
docker build -f Dockerfile.flask -t test-app .

# Run locally
docker run -p 8080:8080 test-app

# Check ECR
aws ecr describe-repositories --region us-west-2
```

## 📈 Next Steps

### ECS Deployment
```yaml
# Add to workflow
- name: Deploy to ECS
  run: |
    aws ecs update-service --cluster my-cluster --service my-service --force-new-deployment
```

### Kubernetes Deployment
```yaml
# Add to workflow
- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/my-app my-app=${{ steps.login-ecr.outputs.registry }}/my-app:latest
```

### Monitoring Integration
- Add CloudWatch metrics
- Set up alerts
- Configure logging

## 🎯 Benefits

✅ **Automated Testing** - Every change is tested  
✅ **Consistent Builds** - Same environment every time  
✅ **Security** - Non-root containers, minimal attack surface  
✅ **Scalability** - Cloud-based builds, no local resource usage  
✅ **Traceability** - Git SHA tags, environment tracking  
✅ **Rollback** - Multiple image versions available  

---

**Ready to deploy!** 🚀

Push your changes to trigger the pipeline, or use the manual workflow trigger to test the deployment process. 