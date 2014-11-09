package org.apache.oodt.pge.examples.pgetask.writers;

import java.io.File;
import java.util.logging.Logger;

import org.apache.oodt.cas.metadata.Metadata;
import org.apache.oodt.cas.metadata.extractors.FilenameTokenMetExtractor;
import org.apache.oodt.cas.pge.writers.PcsMetFileWriter;

public class PGETaskExtractorWriter extends PcsMetFileWriter {

	private static final Logger LOG = Logger.getLogger(PGETaskExtractorWriter.class
		      .getName());	
	
	@Override
	protected Metadata getSciPgeSpecificMetadata(File sciPgeCreatedDataFile,
			Metadata inputMetadata, Object... customArgs) throws Exception {

		Metadata met = new Metadata();
		met.addMetadata(inputMetadata);
		met.addMetadata("ProductType", "GenericFile");
		
	    String metConfFilePath = String.valueOf(customArgs[0]);
	    LOG.info("metConfFilePath = ["+metConfFilePath+"]");
	    FilenameTokenMetExtractor extractor = new FilenameTokenMetExtractor();
	    extractor.setConfigFile(metConfFilePath);
	    met.addMetadata(extractor.extractMetadata(sciPgeCreatedDataFile));
	    
		return met;
	}

}
