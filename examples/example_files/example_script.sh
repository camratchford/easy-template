ezt.exe --force true \
  -c "example_files/config.yml" \
  -t "example_files/readme_template.md.j2" \
  -v "title=How do you make a cheeseburger?" \
  --var-file "example_files/vars.yml" \
  -o "example_files/README.md"

