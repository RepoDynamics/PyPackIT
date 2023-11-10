# Discussion Category Forms
[Discussion category forms](https://docs.github.com/en/discussions/managing-discussions-for-your-community/creating-discussion-category-forms)
customize the templates that are available for community members to use
when they open new discussions in the repository.
It encourages community members to include specific, structured information
in their discussions by using customizable web form fields.

To be recognized by GitHub, discussion category forms must be stored in the directory `/.github/DISCUSSION_TEMPLATE/`
(i.e. this directory). Each YAML file defines a form for a specific discussion category, indicated by the
filename, which must correspond with the slug for one of the discussion categories.
For example, the template for the "New Announcements" category should be stored in `.github/DISCUSSION_TEMPLATE/new-announcements.yml`.
Discussion forms, like issue forms, are written in YAML, using the
GitHub [form schema](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema).
