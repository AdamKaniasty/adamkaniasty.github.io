require "json"

module PortfolioSeo
  class Generator < Jekyll::Generator
    safe true
    priority :low

    def generate(site)
      resume = JSON.parse(File.read(File.join(site.source, "assets/json/resume.json")))
      site.data["resume"] = resume
      origin = site.config.fetch("url").sub(%r{/$}, "") + site.config.fetch("baseurl", "")
      person_id = "#{origin}/#person"
      website_id = "#{origin}/#website"
      basics = resume.fetch("basics")
      person = {
        "@type" => "Person", "@id" => person_id, "name" => basics.fetch("name"),
        "url" => "#{origin}/", "image" => "#{origin}/assets/img/personal/me.jpg",
        "description" => basics.fetch("summary"), "jobTitle" => resume.fetch("work").first.fetch("position"),
        "worksFor" => { "@type" => "Organization", "name" => resume.fetch("work").first.fetch("name") },
        "alumniOf" => { "@type" => "CollegeOrUniversity", "name" => "Warsaw University of Technology", "url" => "https://www.pw.edu.pl/" },
        "knowsAbout" => ["Software engineering", "Machine learning", "AI agents", "Retrieval-augmented generation", "Reinforcement learning", "Mechanistic interpretability", "Python", "Java", "Kubernetes"],
        "sameAs" => basics.fetch("profiles").map { |profile| profile.fetch("url") }.uniq
      }
      website = { "@type" => "WebSite", "@id" => website_id, "url" => "#{origin}/", "name" => basics.fetch("name"), "author" => { "@id" => person_id }, "inLanguage" => "en" }
      pages = site.pages + site.collections.values.flat_map(&:docs)
      pages.each do |page|
        next unless page.data["layout"]
        if page.data["layout"].start_with?("archive-")
          page.data["noindex"] = true
          page.data["sitemap"] = false
          page.data["title"] = "Talk archive: #{page.url.split('/').last}"
          page.data["description"] = "Archived technical talks by Adam Kaniasty. Browse the talks page for recordings and mentoring activities."
        end
        url = "#{origin}#{page.url.sub(/index\.html$/, '')}"
        title = page.data["seo_title"] || (page.url == "/" ? "#{basics['name']} — Software Engineer, AI & Machine Learning" : "#{page.data['title']} | #{basics['name']}")
        description = page.data["description"] || site.config["description"].strip
        page.data["seo_title"] = title
        page.data["seo_description"] = description
        page.data["canonical_url"] = url
        page.data["seo_image"] = "#{origin}#{page.data['og_image'] || site.config['og_image']}"
        type = page.data["schema_type"] || "WebPage"
        graph = [person, website]
        webpage = { "@type" => type, "@id" => "#{url}#webpage", "url" => url, "name" => title, "description" => description, "isPartOf" => { "@id" => website_id }, "inLanguage" => page.data["lang"] || "en" }
        webpage["mainEntity"] = { "@id" => person_id } if type == "ProfilePage"
        if page.respond_to?(:collection) && page.collection.label == "projects"
          work = { "@type" => page.data["github"] ? "SoftwareSourceCode" : "CreativeWork", "@id" => "#{url}#project", "name" => page.data["title"], "description" => description, "url" => url, "creator" => [{ "@id" => person_id }] }
          Array(page.data["contributors"]).each { |name| work["creator"] << { "@type" => "Person", "name" => name } }
          work["codeRepository"] = page.data["github"] if page.data["github"]
          work["programmingLanguage"] = page.data["programming_languages"] if page.data["github"] && page.data["programming_languages"]
          webpage["mainEntity"] = { "@id" => work["@id"] }
          graph << work
        end
        if page.data["research_index"]
          articles = site.data.fetch("research").map do |paper|
            article = {
              "@type" => "ScholarlyArticle", "@id" => paper.fetch("doi_url"), "name" => paper.fetch("title"),
              "url" => paper.fetch("url"), "datePublished" => paper.fetch("year").to_s,
              "identifier" => { "@type" => "PropertyValue", "propertyID" => "DOI", "value" => paper.fetch("doi") },
              "author" => paper.fetch("authors").map { |name| name == basics['name'] ? { "@id" => person_id } : { "@type" => "Person", "name" => name } },
              "isPartOf" => { "@type" => "PublicationIssue", "name" => paper.fetch("venue") },
              "about" => { "@id" => "#{origin}#{paper.fetch('project_url')}#project" }
            }
            graph << article
            { "@id" => article["@id"] }
          end
          webpage["mainEntity"] = articles
        end
        graph << webpage
        unless page.url == "/" || page.data["noindex"]
          crumbs = [{ "@type" => "ListItem", "position" => 1, "name" => "Adam Kaniasty", "item" => "#{origin}/" }]
          if page.url.start_with?("/projects/") && page.url != "/projects/"
            crumbs << { "@type" => "ListItem", "position" => 2, "name" => "Projects", "item" => "#{origin}/projects/" }
          end
          crumbs << { "@type" => "ListItem", "position" => crumbs.length + 1, "name" => page.data["title"], "item" => url }
          graph << { "@type" => "BreadcrumbList", "@id" => "#{url}#breadcrumbs", "itemListElement" => crumbs }
        end
        # Escape '<' so content cannot terminate the script element.
        page.data["json_ld"] = JSON.generate({ "@context" => "https://schema.org", "@graph" => graph }).gsub("<", "\\u003c")
      end
    end
  end
end
