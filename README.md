# web_checker_for_exams


The teacher should be able to specify
 * Where to download repositories from
 * Specify assignment variants, and for each variant specify its tests
 * Specify testing requirements (from a possible list for now) and required scores
 * Check README.md file 
 * Check for presence/absence of certain files in the repo
 * Upload the tests or some information to generate tests


How it should word with existing exam. Algorithm (implementation under ubuntu):
 * Download the repo 
 * Go to the folder
 * Run the script run.sh (it downloads the image and starts the container)
 * Error analysis: 
   * If it's built for another system, make your own build. 
   * There may be a build error - output the text.
   * If there is an error in another build, output the error text.
   * If everything is ok - run the teacher's test - output the result.
 * Check README.md
 * Check for presence/absence of different files in the repository.

As a result, the teacher gets a table with grades. The tacher can check logs in the form of files for each student
