#define REAL_SCRIPT "/home/django-de/svn/django/hooks/post-commit.py"
#include <sys/types.h>
#include <unistd.h>
main( ac, av )
  char **av;
{
  execv( REAL_SCRIPT, av );
}