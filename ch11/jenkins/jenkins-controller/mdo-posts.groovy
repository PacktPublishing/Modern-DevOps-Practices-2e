job('mdo-posts') {
  scm {
    git {
      remote {
        url('https://github.com/bharamicrosystems/mdo-posts.git')
      }
      branch('main')
    }
  }
  steps {
    shell('chmod +x build.sh && ./build.sh bharamicrosystems/posts latest')
  }
}
